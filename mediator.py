"""Mediator pattern
"""
import random
import time


class ControlTower(object):

    def __init__(self):
        self.available_runways = list()
        self.engaged_runways = list()

    def authorize_landing(self):
        if not self.available_runways:
            print("Request denied. No available runways")
            return False

        else:
            runway = self.available_runways.pop()
            self.engaged_runways.append(runway)
            print("Request granted. Please land on runway {}".format(runway))
            self.status()
            return True

    def authorize_takeoff(self):
        # for simplicity, all takeoff requests are granted
        time.sleep(random.randint(0, 2))
        runway = self.engaged_runways.pop()
        self.available_runways.append(runway)
        self.status()

    def status(self):
        print(
            "The control tower has {} available runway/s".format(
                len(self.available_runways)
            )
        )


class Airplane(object):

    def __init__(self):
        self.control_tower = None

    @property
    def registered(self):
        return True if self.control_tower is not None else False

    def register(self, control_tower):
        self.control_tower = control_tower
        print("An airplane registers with the control tower")

    def request_landing(self):
        is_authorized = self.control_tower.authorize_landing()
        if is_authorized:
            self.land()

    def land(self):
        print("The airplane {} lands".format(self))

    def takeoff(self):
        print("The airplane {} takes off".format(self))
        self.control_tower.authorize_takeoff()


class Runway(object):

    def register(self, control_tower):
        print("A runway has been registered with the control tower")
        control_tower.available_runways.append(self)
        control_tower.status()


def main():
    print("There is an airport with 2 runways and a control tower\n")
    r1 = Runway()
    r2 = Runway()
    ct = ControlTower()
    r1.register(ct)
    r2.register(ct)

    print("\n3 airplanes approach the airport and register with the tower")
    a1 = Airplane()
    a2 = Airplane()
    a3 = Airplane()
    a1.register(ct)
    a2.register(ct)
    a3.register(ct)

    print(
        "\nTwo airplanes request for landing. There are enough runways, so "
        "the requests are granted"
    )
    a1.request_landing()
    a2.request_landing()

    print(
        "\nThe third airplane also makes a request for landing. There are no"
        " runways available, so the request is denied"
    )
    a3.request_landing()

    print(
        "\nAfter a while, the first airplane takes off, so now the third "
        "airplane can land"
    )
    a1.takeoff()
    a3.request_landing()


if __name__ == "__main__":
    main()
