import math        #import needed modules
import pyaudio     #sudo apt-get install python-pyaudio
import music
import generate.waves as wv
import generate.sound as sd


print ("Mysynth!")

PyAudio = pyaudio.PyAudio     #initialize pyaudio

bitRate = 48000     #number of frames per second/frameset.
freq = 530     #Hz, waves per second, 261.63=C4-note.
length = 2     #seconds to play sound

if freq > bitRate:
    bitRate = freq+100

numFrames = int(bitRate * length * 2)


w1 = wv.create_square_wave(music.notes.get_note("C2"), numFrames, bitRate)
w2 = wv.create_square_wave(music.notes.get_note("C4"), numFrames, bitRate, math.pi / 4)
w3 = wv.create_sin_wave(music.notes.get_note("C4"), numFrames, bitRate)
w4 = wv.create_sin_wave(music.notes.get_note("D#4"), numFrames, bitRate)
w5 = wv.create_sin_wave(music.notes.get_note("G4"), numFrames, bitRate)


#Phase 1
oscs = [w1, w2, w3, w4, w5]
amps = [1, 1, 3, 3, 3]
data = sd.mix_waveforms(oscs, amps)
output = sd.prepare_audio(data)
waveData = output

#Phase 2
oscs = [w4, w5]
amps = [1, 1]
data = sd.mix_waveforms(oscs, amps)
output = sd.prepare_audio(data)
waveData2 = output


# Transmit audio
p = PyAudio()
stream = p.open(format = pyaudio.paFloat32,
                channels = 1,
                rate = bitRate,
                output = True)

stream.write(waveData)
stream.write(waveData2)
stream.stop_stream()
stream.close()
p.terminate()
