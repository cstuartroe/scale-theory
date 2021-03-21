from src.cli.utils import make_parser, ScaleTheoryError


def quiz_parser(verb):
    return make_parser(
        description=f"Quiz your ability to {verb}",
        duration=True,
        velocity=True,
        channel=True,
    )


def get_guess(r):
    while True:
        guess_str = input("Guess: ")
        if guess_str == "again":
            r.play()
        elif guess_str == "quit":
            raise KeyboardInterrupt
        else:
            return guess_str


def quiz_loop(generator_function, round_class):
    while True:
        answer, kwargs = generator_function()

        r = round_class(**kwargs)

        r.play()

        guess = get_guess(r)

        if guess == answer:
            print("Hooray!")
        else:
            print(f"Darn! It was {answer}")
            while input("Play again? ") in ['y', 'yes']:
                r.play()
