def get_note(name):

    F = {}
    default_note = "C4"

    F["C2"] = 65.41

    F["C3"] = F["C2"] * 2
    F["G3"] = 196.0

    F["C4"] = F["C3"] * 2
    F["C#4"] = 277.18
    F["D4"] = 293.66
    F["D#4"]   = 311.13
    F["E4"] = 329.63
    F["F4"] = 349.23
    F["F#4"] = 369.99
    F["G4"] = F["G3"] * 2
    F["G#4"] = 415.30
    F["A4"] = 440.00
    F["A#4"] = 466.16
    F["B4"] = 493.88

    if not name in F.keys():
        name = default_note


    return F[name]

