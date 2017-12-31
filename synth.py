import math        #import needed modules
import pyaudio     #sudo apt-get install python-pyaudio
import music
import generate.waves as wv
import generate.sound as sd
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import copy

print ("Mysynth!")



bitRate = 48000.0     #number of frames per second/frameset.
freq = 530     #Hz, waves per second, 261.63=C4-note.
length = 0.3     #seconds to play sound

if freq > bitRate:
    bitRate = freq+100

numFrames = int(bitRate * length * 2)
rate = int(bitRate)

stream = sd.create_stream(pyaudio.paFloat32, rate, True)


fm1_amp = 0.02
fm1_ratio = 2

fm1 = wv.Modulation(fm1_amp, 5.0)
am1 = wv.Modulation(0.2, 8.0)
#am2 = wv.Modulation(0.5, 7.0)
#am3 = wv.Modulation(0.4, 3.0)

env1 = wv.Envelope(attack=0.0, decay = 0.01, level1 = 1.0, level2 = 1.0, sustain = 0.0)
tryout = wv.create_env_wave(env1, numFrames, bitRate)

'''
sound1 = wv.SoundObject("square", music.notes.get_note("C2"), am = am1, has_am = True, env = env1, has_env = True)
sound2 = wv.SoundObject("square", music.notes.get_note("C4"), am = am1, has_am = True, env = env1, has_env = True)
sound3 = wv.SoundObject("sin", music.notes.get_note("C4"), am = am1, has_am = True, env = env1, has_env = True)
sound4 = wv.SoundObject("sin", music.notes.get_note("D#4"), fm = fm1, has_fm = True, env = env1, has_env = True)
sound5 = wv.SoundObject("sin", music.notes.get_note("G4"), fm = fm1, has_fm = True, env = env1, has_env = True)
sound6 = wv.SoundObject("sin", music.notes.get_note("A#4"), fm = fm1, has_fm = True, env = env1, has_env = True)

w1 = wv.create_sound(sound1, numFrames, bitRate)
w2 = wv.create_sound(sound2, numFrames, bitRate)
w3 = wv.create_sound(sound3, numFrames, bitRate)
w4 = wv.create_sound(sound4, numFrames, bitRate)
w5 = wv.create_sound(sound5, numFrames, bitRate)
w6 = wv.create_sound(sound6, numFrames, bitRate)
'''

g3s = wv.SoundObject("sin", music.notes.get_note("G3"), fm = fm1, has_fm = True, am = am1, has_am = True, env = env1, has_env = True)
g3s.set_fm(wv.Modulation(fm1_amp, music.notes.get_note("G3")*fm1_ratio))

c4s = copy.copy(g3s)
c4s.set_freq(music.notes.get_note("C4"))
c4s.set_fm(wv.Modulation(fm1_amp, music.notes.get_note("C4")*fm1_ratio))

d4s = copy.copy(g3s)
d4s.set_freq(music.notes.get_note("D4"))
d4s.set_fm(wv.Modulation(fm1_amp, music.notes.get_note("D4")*fm1_ratio))

dd4s = copy.copy(g3s)
dd4s.set_freq(music.notes.get_note("D#4"))
dd4s.set_fm(wv.Modulation(fm1_amp, music.notes.get_note("D#4")*fm1_ratio))

g4s = copy.copy(g3s)
g4s.set_freq(music.notes.get_note("G4"))
g4s.set_fm(wv.Modulation(fm1_amp, music.notes.get_note("G4")*fm1_ratio))

g3 = wv.create_sound(g3s, numFrames, bitRate)
c4 = wv.create_sound(c4s, numFrames, bitRate)
d4 = wv.create_sound(d4s, numFrames, bitRate)
dd4 = wv.create_sound(dd4s, numFrames, bitRate)
g4 = wv.create_sound(g4s, numFrames, bitRate)


#exit(0)
def play_sound():

    aw = sd.AudioWriter(stream)

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

        aw.play_audio(waveData1)
        aw.play_audio(waveData2)
        aw.play_audio(waveData2)

        aw.play_audio(waveData3)
        aw.play_audio(waveData2)
        aw.play_audio(waveData2)

    aw.write_file('pyAudioOutput.wav', bit_rate=int(bitRate))

def exit_program():
    stream.stop_stream()
    stream.close()
    p.terminate()
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


