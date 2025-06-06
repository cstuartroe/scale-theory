from random import randrange
from src.player_utils import Player, BASE_MIDI_NOTE, flatten
from src.cli.utils import make_parser


def get_bass_note(fixed_root, edo_steps):
    if fixed_root:
        return BASE_MIDI_NOTE

    return randrange(69 - edo_steps, 69)


def quiz_parser(verb, fixed_root=True, **kwargs):
    parser = make_parser(
        description=f"Quiz your ability to {verb}",
        duration=True,
        velocity=True,
        channel=True,
        **kwargs,
    )
    if fixed_root:
        parser.add_argument("-F", "--fixed_root", action="store_true",
                            help="Whether to keep a fixed root note")
    return parser


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
            for note_group in notes:
                Player().play_simultaneous(note_group, **midi_params)
        elif guess_str in ["individual", "i"]:
            Player().play_sequential(flatten(notes), **midi_params)
        elif guess_str in ["quit", "q"]:
            raise KeyboardInterrupt
        else:
            return guess_str


def quiz_loop(generator_function):
    tried = 0
    correct = 0

    while True:
        tried += 1
        answer, notes, midi_params = generator_function()

        for note_group in notes:
            Player.play_simultaneous(note_group, **midi_params)

        guess = get_guess("Guess: ", notes, midi_params)

        if guess == answer or guess in answer.split("/"):
            print("Hooray!")
            correct += 1
        else:
            print(f"Darn! It was {answer}")

        print(f"{correct}/{tried} ({round(100*correct/tried)}%)")

        get_guess("Hear again? ", notes, midi_params)
