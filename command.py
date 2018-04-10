"""Command pattern

The Command pattern is handy when we want to isolate the portion of the code
that executes an action, from the one that requests the execution. Command can
be useful when we want to create a batch of operations and execute them later.
"""
import datetime
from copy import deepcopy


def rename_command(x, y, *args, **kwargs):
    undo = kwargs.get("undo", False)
    if not undo:
        print("rename {} into {}".format(x, y))
    else:
        print("rename {} into {}".format(y, x))


def move_command(x, source, dest, *args, **kwargs):
    undo = kwargs.get("undo", False)
    if not undo:
        print("move {} from {} to {}".format(x, source, dest))
    else:
        print("move {} from {} to {}".format(x, dest, source))


class Queue(object):

    def __init__(self):
        self._commands = list()
        self._history = list()

    def add_command(self, func, *args, **kwargs):
        timestamp = datetime.datetime.now().isoformat()
        self._commands.append(
            {"timestamp": timestamp, "func": func, "args": args, "kwargs": kwargs}
        )

    def execute(self, commands=None):
        if commands is None:
            commands = self._commands
        for cmd in commands:
            func = cmd["func"]
            args, kwargs = cmd["args"], cmd["kwargs"]
            func(*args, **kwargs)
        self.update_history(commands)
        self.clear_queue()

    def redo(self):
        commands = self._history[-1]
        self.execute(commands)

    def undo(self):
        original_commands = self._history[-1]
        commands = deepcopy(original_commands)
        for cmd in commands:
            func = cmd["func"]
            args, kwargs = cmd["args"], cmd["kwargs"]
            # we need to store the "undo" within the command (for history)
            kwargs.update({"undo": True})
            func(*args, **kwargs)
        self.update_history(commands)

    def clear_queue(self):
        self._commands = list()

    def update_history(self, commands):
        self._history.append(commands)

    def history(self):
        for i, commands in enumerate(self._history):
            print("Set of commands {}".format(i))
            for cmd in commands:
                t = cmd["timestamp"]
                f = cmd["func"].__name__
                ar, kw = cmd["args"], cmd["kwargs"]
                print(" {} - f: {} args: {} kwargs: {}".format(t, f, ar, kw))


def main():
    queue = Queue()

    queue.add_command(rename_command, "test.py", "hello.py")
    queue.add_command(move_command, "hello.py", source="/lib", dest="/home")
    queue.add_command(rename_command, x="readme.txt", y="README.txt")

    print("Execute all commands as a single operation")
    queue.execute()

    print("\nRedo last operation")
    queue.redo()

    print("\nUndo last operation")
    queue.undo()

    print("\nExecute a single command")
    queue.add_command(move_command, "hello.py", source="/lib", dest="/home")
    queue.execute()

    print("\nUndo last operation")
    queue.undo()

    print("\nShow history")
    queue.history()


if __name__ == "__main__":
    main()
