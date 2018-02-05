def get_note(name):

    F = {}
    default_note = "C4"

    # Octave 2
    base_notes = [65.41,
                  69.295,
                  73.415,
                  77.78,
                  82.4075,
                  87.3075,
                  92.5,
                  98.0,
                  103.825,
                  110.0,
                  116.54,
                  123.47]


    # Octave 2
    F["C2"]     = base_notes[0]
    F["C#2"]    = base_notes[1]
    F["D2"]     = base_notes[2]
    F["D#2"]    = base_notes[3]
    F["E2"]     = base_notes[4]
    F["F2"]     = base_notes[5]
    F["F#2"]    = base_notes[6]
    F["G2"]     = base_notes[7]
    F["G#2"]    = base_notes[8]
    F["A2"]     = base_notes[9]
    F["A#2"]    = base_notes[10]
    F["B2"]     = base_notes[11]

    # Octave 3
    F["C3"] = F["C2"] * 2.0
    F["C#3"] = F["C#2"] * 2
    F["D3"] = F["D2"] * 2
    F["D#3"] = F["D#2"] * 2
    F["E3"] = F["E2"] * 2
    F["F3"] = F["F2"] * 2
    F["F#3"] = F["F#2"] * 2
    F["G3"] = F["G2"] * 2
    F["G#3"] = F["G#2"] * 2
    F["A3"] = F["A2"] * 2
    F["A#3"] = F["A#2"] * 2
    F["B3"] = F["B2"] * 2

    # Octave 4
    F["C4"] = F["C3"] * 2
    F["C#4"] = F["C#3"] * 2
    F["D4"] = F["D3"] * 2
    F["D#4"] = F["D#3"] * 2
    F["E4"] = F["E3"] * 2
    F["F4"] = F["F3"] * 2
    F["F#4"] = F["F#3"] * 2
    F["G4"] = F["G3"] * 2
    F["G#4"] = F["G#3"] * 2
    F["A4"] = F["A3"] * 2
    F["A#4"] = F["A#3"] * 2
    F["B4"] = F["B3"] * 2

    # Octave 5
    F["C5"] = F["C4"] * 2
    F["C#5"] = F["C#4"] * 2
    F["D5"] = F["D4"] * 2
    F["D#5"] = F["D#4"] * 2
    F["E5"] = F["E4"] * 2
    F["F5"] = F["F4"] * 2
    F["F#5"] = F["F#4"] * 2
    F["G5"] = F["G4"] * 2
    F["G#5"] = F["G#4"] * 2
    F["A5"] = F["A4"] * 2
    F["A#5"] = F["A#4"] * 2
    F["B5"] = F["B4"] * 2

    if not name in F.keys():
        name = default_note



    #freq = F[name]
    #print("name: " + name + ", freq: " + str(freq))
    return F[name]

