import sys
import cmd
from src.cli import TimeScaleFinding

COMMANDS = {
    "time_scale_finding": TimeScaleFinding,
}


def run_command(command):
    def f(argstring):
        try:
            namespace = command.parser.parse_args(argstring.split())
        except SystemExit:
            return  # argparse likes to SystemExit after --help is called
        kwargs = vars(namespace)
        command.run(**kwargs)

    return f


class ExplorerShell(cmd.Cmd):
    intro = "Welcome to the Scale Explorer.\nEnter 'help' to see a list of commands."
    prompt = "\n$> "

    def __init__(self):
        super().__init__()

        for command_name, command in COMMANDS.items():
            command.parser.prog = command_name
            setattr(self, "do_" + command_name, run_command(command))

    def do_help(self, arg):
        for name, command in COMMANDS.items():
            print(name)
            print(command.parser.format_help())


if __name__ == "__main__":
    ExplorerShell().cmdloop()
