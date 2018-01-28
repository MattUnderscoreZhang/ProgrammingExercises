note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
solfege = ["Do", "Re", "Mi", "Fa", "So", "La", "Ti"]
major_steps = [0, 2, 4, 5, 7, 9, 11]

def note(scale, solfege_note):
    start_position = note_names.index(scale)
    steps = major_steps[solfege.index(solfege_note)]
    note_position = (start_position + steps) % 12
    return note_names[note_position]

if __name__ == "__main__":
    print note("C", "Do")
    print note("C", "Re")
    print note("C", "Mi")
    print note("D", "Mi")
    print note("A#", "Fa")
