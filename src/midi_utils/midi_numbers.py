NOTES_12_EDO = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def get_12_edo_name(midi_number):
    letter = NOTES_12_EDO[midi_number % 12]
    octave = (midi_number//12) - 1
    return f"{letter}{octave}"


BASE_31EDO_MIDI_NOTE = 40


def get_midi_numbers(scale_name, edo):
    scale = SCALE_REFS[edo][scale_name]
    out = [BASE_31EDO_MIDI_NOTE - edo]
    for _ in range(3):
        for interval in scale:
            out.append(out[-1] + interval)
    return out
