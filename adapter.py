class Smartphone(object):

    correct_input_voltage = 5

    def __init__(self, power_source):
        self.input_voltage = power_source.output_voltage

    def charge(self):
        if self.input_voltage > self.correct_input_voltage:
            print("BURNING!!!")
        else:
            print("Charging...")


class Socket(object):
    output_voltage = 230


class Adapter(object):
    input_voltage = Socket.output_voltage
    output_voltage = Smartphone.correct_input_voltage


def main():
    phone = Smartphone(Socket)
    phone.charge()
    phone = Smartphone(Adapter)
    phone.charge()

if __name__ == '__main__':
    main()
