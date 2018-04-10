"""Memento pattern
"""


class Originator(object):
    """Originator is some object that has an internal state.
    The Originator knows how to save and restore itself, but it's the Caretaker
    than controls when to save and restore the Originator."""

    def __init__(self):
        self._state = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    def save(self):
        """Create a Memento and copy the Originator state in it."""
        return Memento(self.state)

    def restore(self, memento):
        """Restore the Originator to a previous state (stored in Memento)."""
        self.state = memento.state


class Memento(object):
    """Memento is an opaque object that holds the state of an Originator."""

    def __init__(self, state):
        self._state = state

    @property
    def state(self):
        return self._state


# Client, the Caretaker of the Memento pattern.
# The Caretaker is going to do something to the Originator, but wants to be
# able to undo the change.
# The Caretaker holds the Memento but cannot change it (Memento is opaque).
# The Caretaker knows when to save and when to restore the Originator.


def main():
    originator = Originator()
    originator.state = "State1"
    memento1 = originator.save()
    originator.state = "State2"
    memento2 = originator.save()
    originator.state = "State3"
    originator.state = "State4"

    originator.restore(memento1)
    assert originator.state == "State1"
    print(originator.state)

    originator.restore(memento2)
    assert originator.state == "State2"
    print(originator.state)


if __name__ == "__main__":
    main()
