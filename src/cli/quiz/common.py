from src.cli.utils import make_parser, ScaleTheoryError


def quiz_parser(verb):
    return make_parser(
        description=f"Quiz your ability to {verb}",
        duration=True,
        velocity=True,
        channel=True,
    )


def get_guess(r, choices):
    while True:
        guess_str = input("Guess: ")
        if guess_str == "again":
            r.play()
        elif guess_str == "quit":
            raise KeyboardInterrupt
        elif guess_str in choices:
            return guess_str
        else:
            print("Must be one of:", ", ".join(choices))


def quiz_loop(generator_function, round_class, choices):
    while True:
        answer, kwargs = generator_function()

        r = round_class(**kwargs)

        r.play()

        guess = get_guess(r, choices)

        if guess == answer:
            print("Hooray!")
        else:
            print(f"Darn! It was {answer}")
            while input("Play again? ") in ['y', 'yes']:
                r.play()
