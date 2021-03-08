import cmd2
import shlex
from src.cli import TimeScaleFinding, ScaleInfo, PrintFamily, ListCycles, ListSubcycles
from src.cli.utils import resolve

COMMANDS = {
    "time_scale_finding": TimeScaleFinding,
    "scale_info": ScaleInfo,
    "print_family": PrintFamily,
    "find_scales": ListCycles,
    "find_subscales": ListSubcycles,
}


def run_command(command):
    def f(argstring):
        try:
            namespace = command.parser.parse_args(shlex.split(argstring))
        except SystemExit:
            return  # argparse likes to SystemExit after --help is called
        except ValueError as e:
            print(e)
            return
        kwargs = resolve(namespace)
        command.run(**kwargs)

    return f


class ExplorerShell(cmd2.Cmd):
    intro = "Welcome to the Scale Explorer.\nEnter 'help' to see a list of commands."
    prompt = "\n$> "

    def __init__(self):
        super().__init__(persistent_history_file="~/.scale_theory_history")

        for command_name, command in COMMANDS.items():
            command.parser.prog = command_name
            setattr(self, "do_" + command_name, run_command(command))

    def do_help(self, arg):
        for name, command in COMMANDS.items():
            print(name)


if __name__ == "__main__":
    ExplorerShell().cmdloop()
