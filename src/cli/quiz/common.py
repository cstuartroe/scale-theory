from random import randrange
from src.midi_utils import emit_midi_notes, emit_midi_sequence
from src.cli.utils import make_parser


def get_bass_note(edo_steps):
    return randrange(52 - edo_steps, 52 + edo_steps)


def quiz_parser(verb, **kwargs):
    return make_parser(
        description=f"Quiz your ability to {verb}",
        duration=True,
        velocity=True,
        channel=True,
        **kwargs,
    )


explained_again = False
explained_individual = False


def get_guess(prompt, notes, midi_params):
    while True:
        global explained_again, explained_individual
        if not explained_again:
            print("Enter `again` to hear again")
            explained_again = True
        if len(notes) == 1 and not explained_individual:
            print("Enter `individual` to hear individual notes")
            explained_individual = True

        guess_str = input(prompt).lower()
        if guess_str in ["again", "y", "yes"]:
            emit_midi_notes(notes, **midi_params)
        elif guess_str in ["individual", "i"]:
            emit_midi_sequence(notes[0], **midi_params)
        elif guess_str in ["quit", "q"]:
            raise KeyboardInterrupt
        else:
            return guess_str


def quiz_loop(generator_function):
    while True:
        answer, notes, midi_params = generator_function()

        emit_midi_notes(notes, **midi_params)

        guess = get_guess("Guess: ", notes, midi_params)

        if guess == answer:
            print("Hooray!")
        else:
            print(f"Darn! It was {answer}")

        get_guess("Hear again? ", notes, midi_params)
