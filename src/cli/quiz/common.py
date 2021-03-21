from random import randrange
from src.midi_utils import emit_midi_notes
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


def get_guess(notes):
    while True:
        guess_str = input("Guess: ")
        if guess_str == "again":
            emit_midi_notes(notes)
        elif guess_str == "quit":
            raise KeyboardInterrupt
        else:
            return guess_str


def quiz_loop(generator_function):
    while True:
        answer, notes, midi_params = generator_function()

        emit_midi_notes(notes)

        guess = get_guess(notes)

        if guess == answer:
            print("Hooray!")
        else:
            print(f"Darn! It was {answer}")
            while True:
                play_again = input("Play again? ")
                if play_again in ['y', 'yes']:
                    emit_midi_notes(notes)
                elif play_again == "quit":
                    raise KeyboardInterrupt
                else:
                    break
