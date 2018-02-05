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

fm1 = wv.Modulation(amp=fm1_amp, mod_ratio = 1.0)
am1 = wv.Modulation(0.2, 8.0)

env1 = wv.Envelope(attack=0.07, decay = 0.7, level1 = 1.0, level2 = 0.7, sustain = 0.0)

sound1 = wv.SoundObject("sin", fm = fm1, has_fm = True, am = am1, has_am = True, env = env1, has_env = True)
sound1.set_fm(wv.Modulation(fm1_amp, fm1_ratio, t=fm1_type))

env2 = wv.Envelope(attack=0.01, decay = 0.03, level1 = 1.0, level2 = 0.15, sustain = 0.0)
sound2 = wv.SoundObject("sin", has_fm = False, am = am1, has_am = True, env = env2, has_env = True)

sound3 = wv.SoundObject("sin", has_fm = False, am = am1, has_am = True, env = env1, has_env = True)




def play_sound():

    # Create audio interface
    aw = sd.AudioDataInterface(bit_rate=rate, play_method='flush')

    bar = length

    # Create channel for each sound
    ch1 = wv.Channel(sobj= sound1, bit_rate=bitRate)
    ch2 = wv.Channel(sobj=sound2, bit_rate=bitRate)
    ch3 = wv.Channel(sobj=sound3, bit_rate=bitRate)

    ch1.add_notes(length=bar, notes="G3")
    ch1.add_notes(length=bar, notes="B3")
    ch1.add_notes(length=bar, notes=["D4", "F4"], amps = [1, 1])

    ch1.multiply(4)

    ch2.add_notes(length=bar, notes="G5")
    ch2.add_notes(length=bar, notes="F#5")
    ch2.add_notes(length=bar, notes="F5")
    ch2.add_notes(length=bar, notes="E5")
    ch2.add_notes(length=bar/3, notes="D#5")
    ch2.add_notes(length=bar/3, notes="E5")
    ch2.add_notes(length=bar/3, notes="D#5")
    ch2.add_notes(length=bar, notes="D5")

    ch2.add_notes(length=bar, notes="D5")
    ch2.add_notes(length=bar, notes="C#5")
    ch2.add_notes(length=bar, notes="D5")
    ch2.add_notes(length=bar, notes="D#5")
    ch2.add_notes(length=bar, notes="D5")
    ch2.add_notes(length=bar, notes="C#5")

    ch3.add_notes(length=bar * 3, notes="G2")
    ch3.add_notes(length=bar * 3, notes="D#2")
    #ch3.add_notes(length=bar * 3, notes="G2")
    #ch3.add_notes(length=bar * 3, notes="B2")


    oscs = [ch1.get_data(), ch2.get_data(), ch3.get_data()]
    amps = [0.5, 1, 0.7]

    master_output = sd.mix_waveforms(oscs, amps)

    aw.append_sound(master_output)

    aw.flush_audio(rate, file='pyAudioOutput.wav')

#g4_data = sd.prepare_audio(g4, debug=False)
#plt.figure()
#plt.plot(g4)
#plt.plot(g4_data)
#plt.show()
#sd.play_buffered(g4_data, rate)


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



