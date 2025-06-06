import platform
import time
from typing import Iterable
from .midi_numbers import BASE_MIDI_NOTE
# from .pyaudio_utils import play_sine_wave

USE_SCM = (platform.system() == 'Darwin')  # macOS
A4_MIDI_NUMBER = 69  # Nice
A4_FREQUENCY = 440

# simplecoremidi is macOS only
if USE_SCM:
    from simplecoremidi import send_midi


def frequency_from_midi_number(midi_number: int, edo: int):
    return A4_FREQUENCY*(2**((midi_number - A4_MIDI_NUMBER)/edo))


class Player:
    @classmethod
    def play_simultaneous(cls, midi_numbers: Iterable[int], edo: int, note_duration: int = 500, velocity: int = 64,
                          channel: int = 0):
        if USE_SCM:
            cls.emit_midi(midi_numbers, note_duration, velocity, channel)
        else:
            cls.play_pyaudio(midi_numbers, edo, note_duration, velocity/128)

    @classmethod
    def play_pyaudio(cls, midi_numbers: Iterable[int], edo: int, note_duration: int = 500, volume: float = .5):
        frequencies = [
            frequency_from_midi_number(mn, edo)
            for mn in midi_numbers
        ]

        # play_sine_wave(frequencies, duration=note_duration, volume=volume)

    @classmethod
    def emit_midi(cls, midi_numbers: Iterable[int], note_duration: int = 500, velocity: int = 64, channel: int = 0):
        for midi_number in midi_numbers:
            send_midi((144 + channel, midi_number, velocity))
        try:
            time.sleep(note_duration / 1000)
        except KeyboardInterrupt:
            for midi_number in midi_numbers:
                send_midi((128 + channel, midi_number, velocity))
            raise
        for midi_number in midi_numbers:
            send_midi((128 + channel, midi_number, velocity))

    @classmethod
    def play_note(cls, midi_number: int, edo: int, note_duration: int = 500, velocity: int = 64,
                  channel: int = 0):
        cls.play_simultaneous([midi_number], edo, note_duration, velocity, channel)

    @classmethod
    def play_sequential(cls, midi_numbers: Iterable[int], edo: int, note_duration: int = 500, velocity: int = 64,
                        channel: int = 0):
        for midi_number in midi_numbers:
            cls.play_note(midi_number, edo, note_duration, velocity, channel)


def sequence_from_jumps(jumps: Iterable[int], starting_note: int = BASE_MIDI_NOTE):
    seq: list[int] = [starting_note]
    for jump in jumps:
        seq.append(seq[-1] + jump)
    return seq


# Pianoteq needs to be waken up every time I start a new process for some reason
# emit_midi([0])
