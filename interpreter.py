import inspect
from pyparsing import Word, OneOrMore, Optional, Group, Suppress, alphanums


class DeviceNotAvailable(Exception):
    pass


class ActionNotAvailable(Exception):
    pass


class IncorrectAction(Exception):
    pass


class Device(object):

    def __call__(self, *args):
        action = args[0]
        try:
            method = getattr(self, action)
        except AttributeError:
            raise ActionNotAvailable(
                '!!! "{}" not available for {}'.format(action, self.__class__.__name__)
            )

        signature = inspect.signature(method)
        # arity of the device's method (excluding self)
        arity = len(signature.parameters.keys())
        # or alternatively
        # arity = method.__code__.co_argcount -1
        # arity = len(inspect.getfullargspec(method)[0]) - 1

        num_args = len([a for a in args if a is not None])
        if arity != num_args - 1:
            parameters = list(signature.parameters.keys())
            if parameters:
                substring = "these parameters {}".format(parameters)
            else:
                substring = "no parameters"
            err_msg = '!!! "{}" on {} must be defined with {}'.format(
                action, self.__class__.__name__, substring
            )
            raise IncorrectAction(err_msg)

        else:
            if num_args == 1:
                method()
            elif num_args == 2:
                method(int(args[1]))
            else:
                raise Exception


class Garage(Device):

    def __init__(self):
        self.is_open = False

    def open(self):
        print("opening the garage")
        self.is_open = True

    def close(self):
        print("closing the garage")
        self.is_open = False


class Boiler(Device):

    def __init__(self):
        self.temperature = 83

    def heat(self, amount):
        print("heat the boiler up by {} degrees".format(amount))
        self.temperature += amount

    def cool(self, amount):
        print("cool the boiler down by {} degrees".format(amount))
        self.temperature -= amount


class Television(Device):

    def __init__(self):
        self.is_on = False

    def switch_on(self):
        print("switch on the television")
        self.is_on = True

    def switch_off(self):
        print("switch off the television")
        self.is_on = False


class Interpreter(object):

    DEVICES = {"boiler": Boiler(), "garage": Garage(), "television": Television()}

    @staticmethod
    def parse(input_string):
        word = Word(alphanums)
        command = Group(OneOrMore(word))
        token = Suppress("->")
        device = Group(OneOrMore(word))
        argument = Group(OneOrMore(word))
        event = command + token + device + Optional(token + argument)
        parse_results = event.parseString(input_string)
        cmd = parse_results[0]
        dev = parse_results[1]
        cmd_str = "_".join(cmd)
        dev_str = "_".join(dev)
        try:
            val = parse_results[2]
        except IndexError:
            val_str = None
        else:
            val_str = "_".join(val)
        return cmd_str, dev_str, val_str

    def interpret(self, input_string):
        cmd_str, dev_str, val_str = self.parse(input_string)
        try:
            device = self.DEVICES[dev_str]
        except KeyError:
            raise DeviceNotAvailable(
                "!!! {} is not available an available " "device".format(dev_str)
            )

        else:
            device(cmd_str, val_str)


def main():
    interpreter = Interpreter()

    valid_inputs = (
        "open -> garage",
        "heat -> boiler -> 5",
        "cool -> boiler -> 3",
        "switch on -> television",
        "switch off -> television",
    )

    for valid_input in valid_inputs:
        interpreter.interpret(valid_input)

    try:
        interpreter.interpret("read -> book")
    except DeviceNotAvailable as e:
        print(e)

    try:
        interpreter.interpret("heat -> boiler")
    except IncorrectAction as e:
        print(e)

    try:
        interpreter.interpret("throw away -> television")
    except ActionNotAvailable as e:
        print(e)


if __name__ == "__main__":
    main()
