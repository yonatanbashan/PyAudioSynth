import numpy as np
import matplotlib.pyplot as plt

class Modulation:
    amp = 1.0
    freq = 0.0
    type = "sin"
    phase = 0.0
    debug = False

    def __init__(self, amp, freq, t = "sin", phase = 0.0, debug = False):
        self.amp = amp
        self.freq = freq
        self.type = t
        self.phase = phase
        self.debug = debug

class SoundObject:

    type = "sin"
    freq = 500.0
    phase = 0.0
    fm = None
    am = None
    has_fm = False
    has_am = False
    has_env = False
    env = None

    def __init__(self, t, freq, phase = 0.0, fm = None, am = None, has_fm = False, has_am = False, has_env = False, env = None):
        self.type = t
        self.freq = freq
        self.phase = phase
        self.fm = fm
        self.am = am
        self.has_fm = has_fm
        self.has_am = has_am
        self.has_env = has_env
        self.env = env

    def set_freq(self, freq):
        self.freq = freq

    def set_fm(self, fm):
        self.fm = fm

class Envelope:

    attack = 0.0
    decay = 0.0
    level1 = 1.0
    level2 = 1.0
    sustain = 0.0
    debug = False

    def __init__(self, attack = 0.0, decay = 0.0, level1 = 1.0, level2 = 1.0, sustain = 0.0, debug = False):
        self.attack = attack
        self.decay = decay
        self.level1 = level1
        self.level2 = level2
        self.sustain = sustain
        self.debug = debug


# Creates a wave for modulation (AM or FM)
def create_mod_wave(dc, mod : Modulation, length, bit_rate):

    if mod.type == "sin":
        mod_wave = create_sin_wave(mod.freq, length, bit_rate, mod.phase)
    elif mod.type == "square":
        mod_wave = create_square_wave(mod.freq, length, bit_rate, mod.phase)

    data = mod_wave * dc * mod.amp + dc

    if mod.debug:
        plt.figure()
        plt.plot(data)
        plt.show()

    return data

def create_env_wave(env : Envelope, length, bit_rate):

    attack = env.attack
    decay = env.decay
    level1 = env.level1
    level2 = env.level2
    sustain = env.sustain

    attack = int(attack * bit_rate)
    decay = decay * bit_rate
    sustain = int(sustain * bit_rate)

    data = np.zeros(length)
    data[0:attack] = np.linspace(0, level1, num=attack)
    data[attack:attack+sustain] = level1
    decay_part = np.arange(length-attack-sustain) * (-1) / decay
    data[attack+sustain:] = level2 + (level1-level2)*np.exp(decay_part)
    if env.debug:
        plt.figure()
        plt.plot(data)
        plt.show()


    return data

# Creates a square base wave
def create_square_wave(f, length, bit_rate, phase = 0.0):
    data = create_sin_wave(f, length, bit_rate, phase)
    data = np.sign(data)
    return data

# Creates a sin base wave
def create_sin_wave(f, length, bit_rate, phase = 0.0, f_carrier = 0.0):

    # Create wave with or without FM
    if type(f) is Modulation:
        mod_sine = np.sin( 2.0 * np.pi * f.freq * np.arange(length) / bit_rate)
        freq_wave = 2.0 * np.pi * f_carrier + f_carrier * f.amp * mod_sine
        data = np.sin( np.multiply(freq_wave, np.arange(length)) / bit_rate + phase   )
    else:
        data = np.sin(2.0 * np.pi * np.arange(length) * f / bit_rate + phase)

    return data

# Generates a buffer for a sin wave
def create_sound(sobj: SoundObject, length, bit_rate):

    f = sobj.freq
    phase = sobj.phase
    stype = sobj.type

    # Replace freq with FM if applied
    if sobj.has_fm:
        f = sobj.fm

    # Create wave
    if stype == "sin":
        data = create_sin_wave(f, length, bit_rate, phase, sobj.freq)
    elif stype == "square":
        data = create_square_wave(f, length, bit_rate, phase)

    # Create envelope, if exists
    if sobj.has_env:
        env = sobj.env
        env_data = create_env_wave(env, length, bit_rate)
        data *= env_data

    # Implement AM, if exists
    if sobj.has_am:
        am = sobj.am
        mod_wave = create_mod_wave(1, am, length, bit_rate)
        max_amp = np.amax(mod_wave)
        if max_amp > 1:
            mod_wave /= max_amp
        data *= mod_wave


    return data