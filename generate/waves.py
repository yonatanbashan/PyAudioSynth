import numpy as np
import matplotlib.pyplot as plt
import music
import generate.sound as sd
import itertools

class Modulation:

    def __init__(self, amp, mod_ratio, t = "sin", phase = 0.0, debug = False):
        self.amp = amp
        self.mod_ratio = mod_ratio
        self.type = t
        self.phase = phase
        self.debug = debug

class SoundObject:

    def __init__(self, t, phase = 0.0, fm = None, am = None, has_fm = False, has_am = False, has_env = False, env = None):
        self.type = t
        self.phase = phase
        self.fm = fm
        self.am = am
        self.has_fm = has_fm
        self.has_am = has_am
        self.has_env = has_env
        self.env = env

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


class Channel:
    def __init__(self, sobj : SoundObject, bit_rate):
        self.sobj = sobj
        self.bit_rate = bit_rate
        self.data = np.zeros(1)

    # Add a note or notes to the channel
    def add_notes(self, length, notes, amps = []):
        frames = int(self.bit_rate * length)
        if type(notes) == list:

            # Sanity check
            if len(amps) != len(notes):
                print("Error: must provide amp list the same size of note list!")
                exit(1)

            oscs = []
            for note in notes:
                new_sound = create_sound(self.sobj, music.notes.get_note(note), frames, self.bit_rate)
                new_sound = sd.smooth_audio(new_sound)
                oscs.append(new_sound)
                if not amps:
                    amps.append(1)

            new_data = sd.mix_waveforms(osc_list= oscs, amp_list = amps)
        else:
            new_sound = create_sound(self.sobj, music.notes.get_note(notes), frames, self.bit_rate)
            new_sound = sd.smooth_audio(new_sound)
            new_data = sd.mix_waveforms(osc_list = [new_sound], amp_list = [1])

        self.data = np.append(self.data, new_data)

    def multiply(self, num = 2):
        new_data = self.data
        for i in range(num - 1):
            self.data = np.append(self.data, new_data)




    def get_data(self):
        return self.data









# Creates a wave for modulation (AM or FM)
def create_mod_wave(dc, base_freq, mod : Modulation, length, bit_rate):

    freq = base_freq * mod.mod_ratio

    if mod.type == "sin":
        mod_wave = create_sin_wave(freq, length, bit_rate, mod.phase)
    elif mod.type == "square":
        mod_wave = create_square_wave(freq, length, bit_rate, mod.phase)

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
def create_square_wave(f, length, bit_rate, phase = 0.0, freq = 0.0):
    data = create_sin_wave(f, length, bit_rate, phase, freq)
    data = np.sign(data)
    return data


# Creates a sin base wave
def create_sin_wave(f, length, bit_rate, phase = 0.0, f_carrier = 0.0):

    # Create wave with or without FM
    if type(f) is Modulation:
        freq = f.mod_ratio * f_carrier
        if f.type == "sin":
            mod_wave = np.sin( 2.0 * np.pi * freq * np.arange(length) / bit_rate)
        if f.type == "square":
            mod_wave = create_square_wave(freq, length, bit_rate, f.phase)
        freq_wave = 2.0 * np.pi * f_carrier + f_carrier * f.amp * mod_wave
        data = np.sin( np.multiply(freq_wave, np.arange(length)) / bit_rate + phase   )
    else:
        data = np.sin(2.0 * np.pi * np.arange(length) * f / bit_rate + phase)

    return data


# Generates a buffer for a sin wave
def create_sound(sobj: SoundObject, freq, length, bit_rate, debug = False):

    phase = sobj.phase
    stype = sobj.type

    # Replace freq with FM if applied
    if sobj.has_fm:
        fm_freq = sobj.fm
    else:
        fm_freq = freq

    # Create wave
    if stype == "sin":
        data = create_sin_wave(fm_freq, length, bit_rate, phase, freq)
    elif stype == "square":
        data = create_square_wave(fm_freq, length, bit_rate, phase, freq)

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