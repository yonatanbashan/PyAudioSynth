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

bitRate = 48000     #number of frames per second/frameset.
length = 0.35     #seconds to play sound

rate = int(bitRate)

# Define sounds
fm1_amp = 0.03
fm1_ratio = 0.5
fm1_type = "sin"

fm1 = wv.Modulation(amp=fm1_amp, mod_ratio = 0.5)
am1 = wv.Modulation(amp=0.2, mod_ratio=8.0)
am2 = wv.Modulation(amp=0.4, mod_ratio=0, direct_freq = 8)

env1 = wv.Envelope(attack=0.07, decay = 0.7, level1 = 1.0, level2 = 0.7, sustain = 0.0)

sound1 = wv.SoundObject("sin", fm = fm1, am = am1, env = env1)
sound1.set_fm(wv.Modulation(fm1_amp, fm1_ratio, t=fm1_type))

env2 = wv.Envelope(attack=0.01, decay = 0.14, level1 = 1.0, level2 = 0.07, sustain = 0.0)
sound2 = wv.SoundObject("tri", am = am1, env = env2, tri_shape = 0.01)

sound3 = wv.SoundObject("sin", am = am1, env = env1)

sound4 = wv.SoundObject("sin", fm = fm1, am = am2, env = env1)


# Usage for example
def play_sound():

    # Create audio interface
    aw = sd.AudioDataInterface(bit_rate=rate, play_method='flush')

    bar = length

    # Create channel for each sound
    ch1 = wv.Channel(sobj=sound4, bit_rate=bitRate)
    ch2 = wv.Channel(sobj=sound2, bit_rate=bitRate)
    ch3 = wv.Channel(sobj=sound3, bit_rate=bitRate)
    
    sheet1 = wv.NoteSheet()
    sheet2 = wv.NoteSheet()
    sheet3 = wv.NoteSheet()

    for i in range(4):
        sheet1.add_notes(length=bar, notes="G4")
        sheet1.add_notes(length=bar, notes="B4")
        sheet1.add_notes(length=bar, notes=["D5", "F5"], amps = [1, 1])

    for i in range(2):
        sheet1.add_notes(length=bar, notes="C4")
        sheet1.add_notes(length=bar, notes="E4")
        sheet1.add_notes(length=bar, notes=["G4", "C5"], amps = [1, 1])

    for i in range(2):
        sheet1.add_notes(length=bar, notes="B3")
        sheet1.add_notes(length=bar, notes="E4")
        sheet1.add_notes(length=bar, notes=["G4", "C5"], amps = [1, 1])

    for i in range(2):
        sheet1.add_notes(length=bar, notes="A3")
        sheet1.add_notes(length=bar, notes="E4")
        sheet1.add_notes(length=bar, notes=["G4", "C5"], amps = [1, 1])

    for i in range(2):
        sheet1.add_notes(length=bar, notes="B3")
        sheet1.add_notes(length=bar, notes="D4")
        sheet1.add_notes(length=bar, notes=["F4", "B4"], amps = [1, 1])


    #ch1.multiply(4)

    sheet2.add_notes(length=bar*2, notes="G5")
    sheet2.add_notes(length=bar, notes="G5")
    sheet2.add_notes(length=bar*2, notes="F5")
    sheet2.add_notes(length=bar, notes="F5")
    sheet2.add_notes(length=bar*2, notes="E5")
    sheet2.add_notes(length=bar, notes="E5")
    sheet2.add_notes(length=bar, notes="D5")
    sheet2.add_notes(length=bar, notes="E5")
    sheet2.add_notes(length=bar, notes="A5")

    sheet2.add_notes(length=bar*3, notes="C5")
    sheet2.add_notes(length=bar, notes="C5")
    sheet2.add_notes(length=bar, notes="B4")
    sheet2.add_notes(length=bar, notes="C5")
    sheet2.add_notes(length=bar*3, notes="D5")
    sheet2.add_notes(length=bar, notes="D5")
    sheet2.add_notes(length=bar, notes="C5")
    sheet2.add_notes(length=bar, notes="D5")
    sheet2.add_notes(length=bar*3, notes="E5")
    sheet2.add_notes(length=bar, notes="E5")
    sheet2.add_notes(length=bar, notes="D5")
    sheet2.add_notes(length=bar, notes="E5")
    sheet2.add_notes(length=bar*6, notes="F5")


    sheet3.add_notes(length=bar * 12, notes="G2")
    sheet3.add_notes(length=bar * 6, notes="C3")
    sheet3.add_notes(length=bar * 6, notes="B2")
    sheet3.add_notes(length=bar * 6, notes="A2")
    sheet3.add_notes(length=bar * 3, notes="F2")
    sheet3.add_notes(length=bar * 3, notes="B2")

    ch1.set_sheet(sheet1)
    ch2.set_sheet(sheet2)
    ch3.set_sheet(sheet3)

    ch1.generate_sound()
    ch2.generate_sound()
    ch3.generate_sound()

    oscs = [ch1.get_data(), ch2.get_data(), ch3.get_data()]
    amps = [0.5, 0.5, 0.5]


    master_output = sd.mix_waveforms(oscs, amps)

    aw.append_sound(master_output)

    aw.flush_audio(rate, file='pyAudioOutput.wav')

    #plt.figure()
    #plt.plot(master_output[4000:12000])
    #plt.show()

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



