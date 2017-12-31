import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav

class AudioWriter:

    stream = None
    filedata = None

    def __init__(self, stream):
        self.stream = stream
        self.filedata = np.zeros(1)

    def play_audio(self, data, debug = False):
        stream_data = prepare_audio(data, debug)
        self.stream.write(stream_data)
        if self.filedata is None:
            self.filedata = data
        else:
            self.filedata = np.append(self.filedata, data)

    def write_file(self, file, bit_rate):
        write_data = self.filedata.astype(np.float32)
        wav.write(file, bit_rate, write_data)



# Prepare data for pyAudio required format. Input is a waveform list/array
def prepare_audio(data, debug = False):

    att_size = 500
    att_in = np.linspace(0, 1, num=att_size)
    att_out = np.linspace(1, 0, num=att_size)


    data[0:att_size] = data[0:att_size] * att_in
    data[-att_size:] = data[-att_size:] * att_out

    if debug:
        plt.figure()
        plt.plot(data[-1000:])
        plt.show()

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

def create_stream(sound_format, rate, output):

    # Transmit audio
    PyAudio = pyaudio.PyAudio
    p = PyAudio()
    stream = p.open(format=sound_format,
                    channels=1,
                    rate=rate,
                    output=output,
                    )

    return stream