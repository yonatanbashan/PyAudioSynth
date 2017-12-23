import numpy as np

def create_square_wave(f, waveform_length, bit_rate, phase = 0):
    data = create_sin_wave(f, waveform_length, bit_rate, phase)
    data = np.sign(data)
    return data

# Generates a sin wave with a given frequenct, length, bit rate and phase
def create_sin_wave(f, waveform_length, bit_rate, phase = 0):

    data = np.sin(2 * np.pi * np.arange(waveform_length) * f / bit_rate + phase);
    return data
