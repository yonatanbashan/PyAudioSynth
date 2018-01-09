def get_note(name):

    F = {}
    default_note = "C4"

    F["C2"] = 65.41

    F["C3"] = F["C2"] * 2
    F["G3"] = 196.0
    F["A3"] = 220.0
    F["A#3"] = 233.08

    F["C4"] = F["C3"] * 2
    F["C#4"] = 277.18
    F["D4"] = 293.66
    F["D#4"]   = 311.13
    F["E4"] = 329.63
    F["F4"] = 349.23
    F["F#4"] = 369.99
    F["G4"] = F["G3"] * 2
    F["G#4"] = 415.30
    F["A4"] = F["A3"] * 2
    F["A#4"] = F["A#3"] * 2
    F["B4"] = 493.88

    F["C5"] = F["C4"] * 2

    if not name in F.keys():
        name = default_note


    return F[name]

