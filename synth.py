import math
import pyaudio
import music
import generate.waves as wv
import generate.sound as sd
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import copy
import time

print ("Mysynth!")

bitRate = 48000.0     #number of frames per second/frameset.
freq = 530     #Hz, waves per second, 261.63=C4-note.
length = 0.35     #seconds to play sound

if freq > bitRate:
    bitRate = freq+100

numFrames = int(bitRate * length)
rate = int(bitRate)


fm1_amp = 0.1
fm1_ratio = 0.5
fm1_type = "sin"

fm1 = wv.Modulation(amp=fm1_amp, freq = 5.0)
am1 = wv.Modulation(0.2, 8.0)


env1 = wv.Envelope(attack=0.07, decay = 0.1, level1 = 1.0, level2 = 0.5, sustain = 0.0)
tryout = wv.create_env_wave(env1, numFrames, bitRate)

g3s = wv.SoundObject("sin", music.notes.get_note("G3"), fm = fm1, has_fm = True, am = am1, has_am = True, env = env1, has_env = True)
g3s.set_fm(wv.Modulation(fm1_amp, music.notes.get_note("G3")*fm1_ratio, t=fm1_type))

a3s = copy.copy(g3s)
a3s.set_freq(music.notes.get_note("A3"))
a3s.set_fm(wv.Modulation(fm1_amp, music.notes.get_note("A3")*fm1_ratio, t=fm1_type))

ad3s = copy.copy(g3s)
ad3s.set_freq(music.notes.get_note("A#3"))
ad3s.set_fm(wv.Modulation(fm1_amp, music.notes.get_note("A#3")*fm1_ratio, t=fm1_type))

c4s = copy.copy(g3s)
c4s.set_freq(music.notes.get_note("C4"))
c4s.set_fm(wv.Modulation(fm1_amp, music.notes.get_note("C4")*fm1_ratio, t=fm1_type))

d4s = copy.copy(g3s)
d4s.set_freq(music.notes.get_note("D4"))
d4s.set_fm(wv.Modulation(fm1_amp, music.notes.get_note("D4")*fm1_ratio, t=fm1_type))

dd4s = copy.copy(g3s)
dd4s.set_freq(music.notes.get_note("D#4"))
dd4s.set_fm(wv.Modulation(fm1_amp, music.notes.get_note("D#4")*fm1_ratio, t=fm1_type))

f4s = copy.copy(g3s)
f4s.set_freq(music.notes.get_note("F4"))
f4s.set_fm(wv.Modulation(fm1_amp, music.notes.get_note("F4")*fm1_ratio, t=fm1_type))

g4s = copy.copy(g3s)
g4s.set_freq(music.notes.get_note("G4"))
g4s.set_fm(wv.Modulation(fm1_amp, music.notes.get_note("G4")*fm1_ratio, t=fm1_type))

gd4s = copy.copy(g3s)
gd4s.set_freq(music.notes.get_note("G#4"))
gd4s.set_fm(wv.Modulation(fm1_amp, music.notes.get_note("G#4")*fm1_ratio, t=fm1_type))

c5s = copy.copy(g3s)
c5s.set_freq(music.notes.get_note("C5"))
c5s.set_fm(wv.Modulation(fm1_amp, music.notes.get_note("C5")*fm1_ratio, t=fm1_type))

g3 = wv.create_sound(g3s, numFrames, bitRate)
a3 = wv.create_sound(a3s, numFrames, bitRate)
ad3 = wv.create_sound(ad3s, numFrames, bitRate)
c4 = wv.create_sound(c4s, numFrames, bitRate)
d4 = wv.create_sound(d4s, numFrames, bitRate)
dd4 = wv.create_sound(dd4s, numFrames, bitRate)
f4 = wv.create_sound(f4s, numFrames, bitRate)
g4 = wv.create_sound(g4s, numFrames, bitRate)
gd4 = wv.create_sound(gd4s, numFrames, bitRate)
c5 = wv.create_sound(c5s, numFrames, bitRate)





#g4_data = sd.prepare_audio(g4, debug=False)
#plt.figure()
#plt.plot(g4)
#plt.plot(g4_data)
#plt.show()
#sd.play_buffered(g4_data, rate)

#exit(0)
def play_sound():

    aw = sd.AudioDataInterface(bit_rate=rate, play_method='flush')

    oscs = [c4, d4]
    amps = [1, 0]
    waveData1 = sd.mix_waveforms(osc_list=oscs, amp_list=amps)

    oscs = [dd4, g4]
    amps = [1, 1]
    waveData2 = sd.mix_waveforms(oscs, amps)

    oscs = [g3, d4]
    amps = [1, 0]
    waveData3 = sd.mix_waveforms(oscs, amps)

    for i in range(2):

        aw.append_sound(waveData1)
        aw.append_sound(waveData2)
        aw.append_sound(waveData2)

        aw.append_sound(waveData3)
        aw.append_sound(waveData2)
        aw.append_sound(waveData2)


    oscs = [f4, f4]
    amps = [1, 0]
    waveData1 = sd.mix_waveforms(osc_list=oscs, amp_list=amps)

    oscs = [gd4, c5]
    amps = [1, 1]
    waveData2 = sd.mix_waveforms(oscs, amps)

    oscs = [c4, c4]
    amps = [1, 0]
    waveData3 = sd.mix_waveforms(oscs, amps)

    oscs = [dd4, dd4]
    amps = [1, 0]
    waveData4 = sd.mix_waveforms(oscs, amps)

    oscs = [ad3, ad3]
    amps = [1, 0]
    waveData5 = sd.mix_waveforms(oscs, amps)

    aw.append_sound(waveData1)
    aw.append_sound(waveData2)
    aw.append_sound(waveData2)

    aw.append_sound(waveData3)
    aw.append_sound(waveData2)
    aw.append_sound(waveData4)

    aw.append_sound(waveData1)
    aw.append_sound(waveData2)
    aw.append_sound(waveData2)

    aw.append_sound(waveData3)
    aw.append_sound(waveData2)
    aw.append_sound(waveData5)

    aw.flush_audio(rate, file='pyAudioOutput.wav')

def exit_program():
    #stream.stop_stream()
    #stream.close()
    #p.terminate()
    quit()

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

playButton = tk.Button(frame,
                   text="Play",
                   command=play_sound)
playButton.pack(side=tk.LEFT)
quitButton = tk.Button(frame,
                   text="Quit",
                   command=exit_program)
quitButton.pack(side=tk.LEFT)


root.mainloop()



