import time
from typing import List
# sinplecoremidi is MacOS only - TODO find a more general solution
from simplecoremidi import send_midi
from .midi_numbers import BASE_MIDI_NOTE


def emit_midi(midi_number, duration_ms=500, velocity=64, channel=0):
    send_midi((144 + channel, midi_number, velocity))
    try:
        time.sleep(duration_ms / 1000)
    except KeyboardInterrupt:
        send_midi((128 + channel, midi_number, velocity))
        raise
    send_midi((128 + channel, midi_number, velocity))


def sequence_from_jumps(jumps: List[int], starting_note: int):
    seq: List[int] = [starting_note]
    for jump in jumps:
        seq.append(seq[-1] + jump)
    return seq


# I'm using the free version of pianoteq which dulls some keys
DEAD_KEYS = {0, 1, 5, 6, 10, 11, 15, 16, 17, 42, 44, 46, 85, 87, 90, 92, 94, 116, 117, 121, 122, 123}


def sequence_with_no_dead_keys(jumps, target_starting_note):
    for i in range(20):
        seq = sequence_from_jumps(jumps, starting_note=target_starting_note + i)
        if all(note not in DEAD_KEYS for note in seq):
            return seq

        seq = sequence_from_jumps(jumps, starting_note=target_starting_note - i)
        if all(note not in DEAD_KEYS for note in seq):
            return seq

    return sequence_from_jumps(jumps, target_starting_note)


def emit_midi_sequence(jumps, note_duration, velocity, channel, starting_note=BASE_MIDI_NOTE):
    for note_number in sequence_with_no_dead_keys(jumps, starting_note):
        emit_midi(note_number, duration_ms=note_duration, velocity=velocity, channel=channel)
