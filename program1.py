import generate.waves as wv
import generate.sound as sd

def main_program():

    bitRate = 48000  # number of frames per second/frameset.
    beat = 2.0  # seconds to play sound

    rate = int(bitRate)

    # Define sounds
    fm1_amp = 0.01
    fm1_ratio = 1.0
    fm1_type = "sin"

    fm1 = wv.Modulation(amp=fm1_amp, mod_ratio=0.5)
    fm2 = wv.Modulation(amp=0.005, mod_ratio=2.0, t="sin")

    am1 = wv.Modulation(amp=0.2, mod_ratio=8.0)
    am2 = wv.Modulation(amp=0.4, mod_ratio=0, direct_freq=8)
    env1 = wv.Envelope(attack=0.07, decay=0.7, level1=1.0, level2=0.7, sustain=0.0)

    sound1 = wv.SoundObject("sin", fm=fm1, am=am1, env=env1)
    sound1.set_fm(wv.Modulation(fm1_amp, fm1_ratio, t=fm1_type))

    env2 = wv.Envelope(attack=0.01, decay=0.14, level1=1.0, level2=0.07, sustain=0.0)
    sound2 = wv.SoundObject("tri", am=am1, env=env2, tri_shape=0.35)
    sound3 = wv.SoundObject("sin", am=am1, env=env1)

    env3 = wv.Envelope(attack=0.4, decay=0.5, level1=1.0, level2=0.3, sustain=0.0)
    sound4 = wv.SoundObject("sin", fm=fm2, am=am2, env=env3, tri_shape=0.2)

    # Create audio interface
    aw = sd.AudioDataInterface(bit_rate=rate, play_method='flush')
    #aw = sd.AudioDataInterface(bit_rate=rate, play_method='write') # If we only want to write file without playing
    bar = beat/4

    # Create channel for each sound
    ch1 = wv.Channel(sobj=sound1, bit_rate=bitRate)
    ch2 = wv.Channel(sobj=sound2, bit_rate=bitRate)
    ch3 = wv.Channel(sobj=sound3, bit_rate=bitRate)
    ch4 = wv.Channel(sobj=sound4, bit_rate=bitRate)

    sheet1 = wv.NoteSheet()
    sheet2 = wv.NoteSheet()
    sheet3 = wv.NoteSheet()
    sheet4 = wv.NoteSheet()

    sheet1 = add_verse(sheet1, bar)

    sheet2 = wv.sync_to_sheet(sheet2, sheet1)
    sheet1 = add_verse(sheet1, bar)
    sheet2 = add_verse_melody(sheet2, bar)


    sheet3 = wv.sync_to_sheet(sheet3, sheet1)
    sheet4 = wv.sync_to_sheet(sheet4, sheet1)
    for i in range(2):
        sheet1 = add_chorus(sheet1, bar, "low")
        sheet4 = add_chorus(sheet4, bar, "high")

    # Bass
    for i in range(2):
        sheet3.add_notes(length=bar * 4, notes="C3")
        sheet3.add_notes(length=bar * 4, notes="F2")
        sheet3.add_notes(length=bar * 4, notes="A#2")
        sheet3.add_notes(length=bar * 4, notes="C#3")

    # Chorus
    for i in range(2):
        sheet2 = add_chorus_melody(sheet2, bar)


    ch1.set_sheet(sheet1)
    ch2.set_sheet(sheet2)
    ch3.set_sheet(sheet3)
    ch4.set_sheet(sheet4)

    channels = [ch1, ch2, ch3, ch4]

    sd.generate_channels(channels)

    ch1_data = ch1.get_data()
    ch2_data = ch2.get_data()
    ch3_data = ch3.get_data()
    ch4_data = ch4.get_data()

    ch2_data = wv.delay_effect(signal=ch2_data, delay_in_seconds=bar/3, coeff=0.7, bitrate=bitRate)

    oscs = [ch1_data, ch2_data, ch3_data, ch4_data]
    amps = [0.5, 0.25, 0.5, 0.2]

    master_output = sd.mix_waveforms(oscs, amps)
    #master_output = wv.cut_audio(master_output, bitrate=bitRate, start=bar*60)


    aw.append_sound(master_output)

    aw.flush_audio(rate, file='pyAudioOutput.wav')


def add_verse_melody(sheet, bar):
    sheet.add_notes(length=bar*3/2, notes = None)
    sheet.add_notes(length=bar/2, notes="C5") # I'm
    sheet.add_notes(length=bar/2, notes="D5") # cro-
    sheet.add_notes(length=bar/2, notes="D5") # ssing
    sheet.add_notes(length=bar/2, notes="C5") # the
    sheet.add_notes(length=bar, notes="E5") # high-
    sheet.add_notes(length=bar * 7 / 2, notes="B4") # way
    sheet.add_notes(length=bar * 3 / 2, notes="D5") # step
    sheet.add_notes(length=bar * 3 / 2, notes="A4") # by
    sheet.add_notes(length=bar * 10 / 2, notes="C5") # step
    sheet.add_notes(length=bar / 2, notes="D5")  # slow
    sheet.add_notes(length=bar / 2, notes="C5")  # and
    sheet.add_notes(length=bar * 3, notes="D5")  # calm
    sheet.add_notes(length=bar / 2, notes="D5") # long
    sheet.add_notes(length=bar / 2, notes="C5") # and
    sheet.add_notes(length=bar / 2, notes="E5") # ru-
    sheet.add_notes(length=bar * 5 / 2, notes="B4") # shing
    sheet.add_notes(length=bar, notes="D5")  # some-
    sheet.add_notes(length=bar * 3 / 2, notes="D5")  # times
    sheet.add_notes(length=bar/2, notes="C5")  #  con
    sheet.add_notes(length=bar/2, notes="E5")  # fu-
    sheet.add_notes(length=bar/2, notes="D5")  # uu-
    sheet.add_notes(length=bar*4, notes="C5")  # sed

    return sheet

def add_verse(sheet, bar):
    sheet.add_notes(length=bar*4, notes=["G3", "C4", "E4"], amps=[1, 1, 1])
    sheet.add_notes(length=bar*4, notes=["G3", "B3", "E4"], amps=[1, 1, 1])
    sheet.add_notes(length=bar*4, notes=["A3", "D4", "F#4"], amps=[1, 1, 1])
    sheet.add_notes(length=bar*4, notes=["A3", "C4", "F4"], amps=[1, 1, 1])
    sheet.add_notes(length=bar * 4, notes=["G3", "C4", "E4"], amps=[1, 1, 1])
    sheet.add_notes(length=bar * 4, notes=["G3", "B3", "E4"], amps=[1, 1, 1])
    sheet.add_notes(length=bar * 4, notes=["A3", "D4", "F#4"], amps=[1, 1, 1])
    sheet.add_notes(length=bar * 4, notes=["A#3", "D4", "F4"], amps=[1, 1, 1])

    return sheet

def add_chorus_melody(sheet, bar):
    sheet.add_notes(length=bar * 3 / 2, notes=["G5", "D4"], amps=[0, 0])  # Silence
    sheet.add_notes(length=bar / 2, notes="C5")
    sheet.add_notes(length=bar, notes="F5")
    sheet.add_notes(length=bar * 5 / 2, notes="C5")
    sheet.add_notes(length=bar / 2, notes="C5")
    sheet.add_notes(length=bar, notes="F5")
    sheet.add_notes(length=bar * 5 / 2, notes="C5")
    sheet.add_notes(length=bar / 2, notes="C5")
    sheet.add_notes(length=bar, notes="G#5")
    sheet.add_notes(length=bar * 5 / 2, notes="G5")
    sheet.add_notes(length=bar / 2, notes="C5")
    sheet.add_notes(length=bar, notes="F5")
    sheet.add_notes(length=bar, notes="C5")

    return sheet

def add_chorus(sheet, bar, height = "low"):
    if height == "low":
        sheet.add_notes(length=bar*4, notes=["G3", "C4", "E4"], amps=[1, 1, 1])
        sheet.add_notes(length=bar*4, notes=["G#3", "C4", "F4"], amps=[1, 1, 1])
        sheet.add_notes(length=bar*4, notes=["F3", "A#4", "D4"], amps=[1, 1, 1])
        sheet.add_notes(length=bar*4, notes=["G#3", "C#4", "F4"], amps=[1, 1, 1])
    else:
        sheet.add_notes(length=bar * 4, notes=["G5", "C5", "E5"], amps=[1, 1, 1])
        sheet.add_notes(length=bar * 4, notes=["G#5", "C5", "F5"], amps=[1, 1, 1])
        sheet.add_notes(length=bar * 4, notes=["F5", "A#5", "D5"], amps=[1, 1, 1])
        sheet.add_notes(length=bar * 4, notes=["G#5", "C#5", "F5"], amps=[1, 1, 1])

    return sheet