import regex

NOTES_12_EDO = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]

LETTERS_TO_NUMBERS_12_EDO = {}
for i, letter in enumerate(NOTES_12_EDO):
    LETTERS_TO_NUMBERS_12_EDO[letter] = i
    for l in letter.split("/"):
        LETTERS_TO_NUMBERS_12_EDO[l] = i

BASE_MIDI_NOTE = 52


def midi_number_to_name(midi_number):
    letter = NOTES_12_EDO[midi_number % 12]
    octave = midi_number//12 - 1
    return f"{letter}{octave}"


def midi_name_to_number(midi_name):
    match = regex.fullmatch(r"([ABCDEFG][b#]?(/[ABCDEFG][b#])?)(-?\d)", midi_name)
    if match:
        letter, _, octave = match.groups()
        if letter in LETTERS_TO_NUMBERS_12_EDO:
            return LETTERS_TO_NUMBERS_12_EDO[letter] + (int(octave) + 1) * 12

    raise ValueError(f"Invalid MIDI note name: {midi_name}")


def midi_number_frequency(midi_number, edo_steps, base_midi_note, base_frequency):
    return round(base_frequency*2**((midi_number - base_midi_note)/edo_steps), 1)


def midi_number_standard_frequency(midi_number):
    return midi_number_frequency(midi_number, 12, 69, 440)
