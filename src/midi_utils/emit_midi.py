import time
from typing import List
# sinplecoremidi is MacOS only - TODO find a more general solution
from simplecoremidi import send_midi
from .midi_numbers import BASE_MIDI_NOTE


def emit_midi(midi_numbers, duration_ms=500, velocity=64, channel=0):
    for midi_number in midi_numbers:
        send_midi((144 + channel, midi_number, velocity))
    try:
        time.sleep(duration_ms / 1000)
    except KeyboardInterrupt:
        for midi_number in midi_numbers:
            send_midi((128 + channel, midi_number, velocity))
        raise
    for midi_number in midi_numbers:
        send_midi((128 + channel, midi_number, velocity))


def sequence_from_jumps(jumps: List[int], starting_note: int = BASE_MIDI_NOTE):
    seq: List[int] = [starting_note]
    for jump in jumps:
        seq.append(seq[-1] + jump)
    return seq


# I'm using the free version of pianoteq which dulls some keys
DEAD_KEYS = {0, 1, 5, 6, 10, 11, 15, 16, 17, 42, 44, 46, 84, 85, 86, 87, 90, 92, 94, 116, 117, 121, 122, 123}


def flatten(l):
    if type(l) == list:
        for e in l:
            yield from flatten(e)
    else:
        yield l


def notes_with_no_dead_keys(notes: List[List[int]]):
    for i in range(20):
        shifted = [[n + i for n in group] for group in notes]
        if all(note not in DEAD_KEYS for note in flatten(shifted)):
            return shifted

        shifted = [[n - i for n in group] for group in notes]
        if all(note not in DEAD_KEYS for note in flatten(shifted)):
            return shifted

    return notes


def emit_midi_notes(notes: List[List[int]], **kwargs):
    for group in notes_with_no_dead_keys(notes):
        emit_midi(group, **kwargs)


def emit_midi_sequence(seq: List[int], **kwargs):
    emit_midi_notes([[n] for n in seq], **kwargs)
