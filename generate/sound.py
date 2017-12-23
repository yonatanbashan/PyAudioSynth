import numpy as np

# Prepare data for pyAudio required format. Input is a waveform list/array
def prepare_audio(data):
    output = data.astype(np.float32)
    return output

# Concatenates waveforms
# osc_list: list of numpy arrays with waveforms.
# amp_list: list of relative amplitudes
def mix_waveforms(osc_list, amp_list):
    amp_list = amp_list / np.sum(amp_list)

    # Multiplying oscs in the amps
    for i, amp in enumerate(amp_list):
        osc_list[i] = osc_list[i] * amp

    # creating new osc by summarizing
    new_osc = np.zeros(len(osc_list[1]))
    for osc in osc_list:
        new_osc = new_osc + osc

    return new_osc