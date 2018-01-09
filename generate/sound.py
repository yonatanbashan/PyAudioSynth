import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import sounddevice as device


def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

# An interface to write data to a file and play
class AudioDataInterface:

    play_method = 'live'
    filedata = None

    def __init__(self, bit_rate, play_method = 'live'):
        self.bit_rate = bit_rate
        self.play_method = play_method
        self.filedata = np.zeros(1)
        device.default.latency = ('low', 'low')
        device.default.dtype = ('float32', 'float32')

    # Appends sound to the output, and plays it if in play_method=='live'
    def append_sound(self, data, debug = False):

        data = prepare_audio(data, debug=debug)

        if self.filedata is None:
            self.filedata = data
        else:

            self.filedata = np.append(self.filedata, data)

        if self.play_method == 'live':
            self.device_play(data, debug=debug)


    # Plays all audio to date and writes data to specified file
    def flush_audio(self, bit_rate, file = None, debug = False):

        if self.play_method == 'flush':
            self.device_play(self.filedata, debug=debug)

        if file:
            self.write_file(file, bit_rate, debug)

    # Writes accumulated data to a file
    def write_file(self, file, bit_rate, debug = False):

        write_data = self.filedata.astype(np.float32)
        wav.write(file, bit_rate, write_data)

        if debug:
            plt.figure()
            plt.plot(write_data)
            plt.title("data to wav file")
            plt.show()





    # Plays data using audio interface
    def device_play(self, data, debug=False):
        device.wait()
        device.play(data, self.bit_rate)

        #(length,) = np.shape(data)
        #length = length / self.bit_rate

        #stream =  device.RawOutputStream(channels=2, dtype='float32', callback=callback)
        #stream.write(data.data)

        if debug:
            plt.figure()
            plt.plot(data)
            plt.title("device_play output")
            plt.show()




# Prepare data for pyAudio required format. Input is a waveform list/array
def prepare_audio(data, dtype=np.float32, debug = False):

    # Create attack (in and out)
    att_size = 500 # TODO: Need to de-hardcode this
    att_in = np.linspace(0, 1, num=att_size)
    att_out = np.linspace(1, 0, num=att_size)
    data[0:att_size] = data[0:att_size] * att_in
    data[-att_size:] = data[-att_size:] * att_out

    # Convert data to desired dtype
    if dtype == np.int16:
        output = data.astype(np.int16)
    elif dtype == np.float32:
        output = data.astype(np.float32)
    else:
        output = data.astype(dtype)

    if debug:
        plt.figure()
        plt.plot(output)
        plt.title("prepare_audio output")
        plt.show()

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


# An attempt to play buffered data
def play_buffered(data, bit_rate):


    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()
    blocksize = 4096*2

    start = 0

    (length,) = np.shape(data)

    # define callback (2)
    def callback(in_data, frame_count, time_info, status):
        nonlocal start
        nonlocal length

        if start+blocksize-1 > length - 1:
            end = length - 1
        else:
            end = start+blocksize-1

        #print(start)
        #print(end)

        dataout = data[start:end]
        start = start + blocksize
        return dataout, pyaudio.paContinue



    # open stream using callback (3)
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=int(bit_rate),
                    output=True,
                    frames_per_buffer=4096,
                    stream_callback=callback)

    # start the stream (4)
    stream.start_stream()


