import re

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
F["C2"] = base_notes[0]
F["C#2"] = base_notes[1]
F["D2"] = base_notes[2]
F["D#2"] = base_notes[3]
F["E2"] = base_notes[4]
F["F2"] = base_notes[5]
F["F#2"] = base_notes[6]
F["G2"] = base_notes[7]
F["G#2"] = base_notes[8]
F["A2"] = base_notes[9]
F["A#2"] = base_notes[10]
F["B2"] = base_notes[11]

notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

for octave in range(3, 8):
    for note in notes:
        lower = note + str(octave - 1)
        name = note + str(octave)
        F[name] = F[lower] * 2

synonyms = dict()
synonyms["Db"] = "C#"
synonyms["Eb"] = "D#"
synonyms["Gb"] = "F#"
synonyms["Ab"] = "G#"
synonyms["Bb"] = "A#"



def get_note(name):

    name = name[0].upper() + name[1:]

    # Separating note name and octave
    name_match = re.search(r'([#A-Z]+)([0-9])', name)
    base_name = name_match.group(1)
    octave = name_match.group(2)

    # Changing to synonym (Ab --> G#, Bb --> A#, etc.)
    if base_name in synonyms.keys():
        base_name = synonyms[base_name]

    # Defining final hash key
    keyname = base_name + octave

    # Default
    if not keyname in F.keys():
        keyname = default_note

    #freq = F[name]
    #print("name: " + name + ", freq: " + str(freq))
    return F[keyname]

