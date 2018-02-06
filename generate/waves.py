import numpy as np
import matplotlib.pyplot as plt
import music
from scipy import signal
import generate.sound as sd
import itertools


# Defines a sequence of notes with lengths and amps
class NoteSheet:

    def __init__(self):
        self.notes = []

    def add_notes(self, length, notes, amps = []):
        if notes is list:
            if not amps:
                amps = np.ones(len(notes))
        else:
            if not amps:
                amps = [1]

        self.notes.append((length, notes, amps))

    def get_notes(self):
        return self.notes



class Modulation:

    def __init__(self, amp, mod_ratio, t = "sin", debug = False, direct_freq = False):
        self.amp = amp
        self.type = t
        self.debug = debug

        # By default, Modulation frequency will be a ratio of the carrier frequenct
        self.mod_ratio = mod_ratio

        # If we want the modulation to be constant and not carrier wave frequency dependent. This is good for AM modulation
        self.direct_freq = direct_freq

class SoundObject:

    def __init__(self, t, fm = None, am = None, env = None, tri_shape = 0.3):
        self.type = t
        self.fm = fm
        self.am = am
        self.env = env
        self.tri_shape = tri_shape
        self.has_fm = False
        self.has_am = False
        self.has_env = False

        if fm:
            self.has_fm = True

        if am:
            self.has_am = True

        if env:
            self.has_env = True

        if self.tri_shape > 0.5 or tri_shape < 0.0:
            raise Exception('tri_shape should be between 0.0 and 0.5')

        if self.has_fm and self.type != 'sin':
            raise Exception('FM modulation is only available for sin waves')




    def set_fm(self, fm):
        self.fm = fm

class Envelope:

    def __init__(self, attack = 0.0, decay = 0.0, level1 = 1.0, level2 = 1.0, sustain = 0.0, debug = False):
        self.attack = attack
        self.decay = decay
        self.level1 = level1
        self.level2 = level2
        self.sustain = sustain
        self.debug = debug


# Holds a SoundObject, a NoteSheet, and generates audio from them
class Channel:
    def __init__(self, sobj : SoundObject, bit_rate, noise = False, noise_amp = 0.0):
        self.sobj = sobj
        self.bit_rate = bit_rate
        self.data = np.zeros(1)
        self.noise = noise
        self.noise_amp = noise_amp
        self.sheet = None

    # Sets the sheet and initializes the data. Whenever this is used, all the previous data is deleted
    def set_sheet(self, sheet : NoteSheet):
        self.sheet = sheet
        self.data = np.zeros(1)

    # Generates the audio from the sheet
    def generate_sound(self):
        self.data = np.zeros(1)
        note_list = self.sheet.get_notes()
        for note_tuple in note_list:
            length = note_tuple[0]
            notes = note_tuple[1]
            if notes is list:
                notes = notes[0]
            amps = note_tuple[2]
            self.add_notes(length, notes, amps)


    # Generates the audio for a note
    def generate_note(self, note, frames):
        new_sound = create_sound(self.sobj, music.notes.get_note(note), frames, self.bit_rate)
        if self.noise:
            noise = create_noise(frames, self.noise_amp)
            new_sound = new_sound + noise
        new_sound = sd.smooth_audio(new_sound)

        return new_sound;


    # Adds the audio data of a note(s) to the channel's data
    def add_notes(self, length, notes, amps = []):
        frames = int(self.bit_rate * length)
        if type(notes) == list:

            # Sanity check
            if len(amps) != len(notes):
                print("Error: must provide amp list the same size of note list!")
                exit(1)

            oscs = []
            for note in notes:
                new_sound = self.generate_note(note, frames)
                oscs.append(new_sound)
                if not amps:
                    amps.append(1)

            new_data = sd.mix_waveforms(osc_list= oscs, amp_list = amps)
        else:
            new_sound = self.generate_note(notes, frames)
            new_data = sd.mix_waveforms(osc_list = [new_sound], amp_list = [1])

        self.data = np.append(self.data, new_data)

    # Multiplies the audio data by a given number
    def multiply(self, num = 2):
        new_data = self.data
        for i in range(num - 1):
            self.data = np.append(self.data, new_data)

    # Returns the audio data
    def get_data(self):
        return self.data









# Creates a wave for modulation (AM or FM)
def create_mod_wave(dc, base_freq, mod : Modulation, length, bit_rate):

    if mod.direct_freq:
        freq = mod.direct_freq
    else:
        freq = base_freq * mod.mod_ratio


    if mod.type == "sin":
        mod_wave = create_sin_wave(freq, length, bit_rate)
    elif mod.type == "square":
        mod_wave = create_square_wave(freq, length, bit_rate)

    data = mod_wave * dc * mod.amp + dc

    if mod.debug:
        plt.figure()
        plt.plot(data)
        plt.show()

    return data

# Creates envelope wave
def create_env_wave(env : Envelope, length, bit_rate):

    # Initialize values
    attack = int(env.attack * bit_rate)
    decay = env.decay * bit_rate
    sustain = int(env.sustain * bit_rate)

    # Attack part
    data = np.zeros(length)
    data[0:attack] = np.linspace(0, env.level1, num=attack)

    # Sustain part
    data[attack:attack+sustain] = env.level1

    # Decay part
    decay_part = np.arange(length - attack - sustain) * (-1) / decay
    data[attack+sustain:] = env.level2 + (env.level1 - env.level2) * np.exp(decay_part)

    if env.debug:
        plt.figure()
        plt.plot(data)
        plt.show()
    return data


# Creates a square base wave
def create_square_wave(f, length, bit_rate, freq = 0.0):
    data = create_sin_wave(f, length, bit_rate, freq)
    data = np.sign(data)
    return data

# Creates a triangle based wave
def create_tri_wave(length, bit_rate, shape, freq = 0.0):


    t = np.linspace(shape, 1-shape, bit_rate/freq) # TODO: Change the 0.4 to 0.6 to parameters of the wave shape
    t_total = t
    while len(t_total) < length:
        t_total = np.append(t_total,t)
    t_total = t_total[0:length]
    triangle = signal.sawtooth(2 * np.pi * 5 * t_total, 0.5)

    return triangle

def create_noise(length, amplitude):

    mu = 0.0 #TODO: Maybe change mu to be a parameter?
    max_sigma = 0.7
    sigma = amplitude
    if sigma > max_sigma:
        sigma = max_sigma
    data = np.random.normal(mu, sigma, length)

    return data


# Creates a sin base wave
def create_sin_wave(f, length, bit_rate, f_carrier = 0.0):

    # Create wave with or without FM
    if type(f) is Modulation:
        freq = f.mod_ratio * f_carrier
        if f.type == "sin":
            mod_wave = np.sin( 2.0 * np.pi * freq * np.arange(length) / bit_rate)
        if f.type == "square":
            mod_wave = create_square_wave(freq, length, bit_rate)
        freq_wave = 2.0 * np.pi * f_carrier + f_carrier * f.amp * mod_wave
        data = np.sin( np.multiply(freq_wave, np.arange(length)) / bit_rate   )
    else:
        data = np.sin(2.0 * np.pi * np.arange(length) * f / bit_rate)

    return data


# Generates a buffer for a sin wave
def create_sound(sobj: SoundObject, freq, length, bit_rate, debug = False):

    stype = sobj.type

    # Replace freq with FM if applied
    if sobj.has_fm:
        fm_freq = sobj.fm
    else:
        fm_freq = freq

    # Create wave
    if stype == "sin":
        data = create_sin_wave(fm_freq, length, bit_rate, freq)
    elif stype == "square":
        data = create_square_wave(fm_freq, length, bit_rate, freq)
    elif stype == "tri":
        shape = sobj.tri_shape
        data = create_tri_wave(length, bit_rate, shape, freq)

    # Create envelope, if exists
    if sobj.has_env:
        env = sobj.env
        env_data = create_env_wave(env, length, bit_rate)
        data *= env_data

    # Implement AM, if exists
    if sobj.has_am:
        am = sobj.am
        mod_wave = create_mod_wave(dc = 1, base_freq = freq, mod = am, length = length, bit_rate = bit_rate)
        max_amp = np.amax(mod_wave)
        if max_amp > 1:
            mod_wave /= max_amp
        data *= mod_wave

    if debug:
        plt.figure()
        plt.plot(data)
        plt.show()

    return data