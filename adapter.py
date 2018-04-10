"""
The Adapter pattern is a structural design pattern. It allows a Client to access
functionalities of a Supplier.
Without an Adapter the Client can not access such functionalities.
This pattern can be implemented with an OBJECT approach or a CLASS approach.
"""


# Client


class Smartphone(object):

    max_input_voltage = 5

    @classmethod
    def outcome(cls, input_voltage):
        if input_voltage > cls.max_input_voltage:
            print("Input voltage: {}V -- BURNING!!!".format(input_voltage))
        else:
            print("Input voltage: {}V -- Charging...".format(input_voltage))

    def charge(self, input_voltage):
        """Charge the phone with the given input voltage."""
        self.outcome(input_voltage)


# Supplier


class Socket(object):
    output_voltage = None


class EUSocket(Socket):
    output_voltage = 230


class USSocket(Socket):
    output_voltage = 120


################################################################################
# Approach A: OBJECT Adapter. The adapter encapsulates client and supplier.
################################################################################


class EUAdapter(object):
    """EUAdapter encapsulates client (Smartphone) and supplier (EUSocket)."""
    input_voltage = EUSocket.output_voltage
    output_voltage = Smartphone.max_input_voltage


class USAdapter(object):
    """USAdapter encapsulates client (Smartphone) and supplier (USSocket)."""
    input_voltage = USSocket.output_voltage
    output_voltage = Smartphone.max_input_voltage


################################################################################
# Approach B: CLASS Adapter. Adapt the Client through multiple inheritance.
################################################################################


class CannotTransformVoltage(Exception):
    """Exception raised by the SmartphoneAdapter.

    This exception represents the fact that an adapter could not provide the
    right voltage to the Smartphone if the voltage of the Socket is wrong."""
    pass


class SmartphoneAdapter(Smartphone, Socket):

    @classmethod
    def transform_voltage(cls, input_voltage):
        if input_voltage == cls.output_voltage:
            return cls.max_input_voltage

        else:
            raise CannotTransformVoltage(
                "Can\'t transform {0}-{1}V. This adapter transforms {2}-{1}V.".format(
                    input_voltage, cls.max_input_voltage, cls.output_voltage
                )
            )

    @classmethod
    def charge(cls, input_voltage):
        try:
            voltage = cls.transform_voltage(input_voltage)
            cls.outcome(voltage)
        except CannotTransformVoltage as e:
            print(e)


class SmartphoneEUAdapter(SmartphoneAdapter, EUSocket):
    """System (smartphone + adapter) for a European Socket.

    Note: SmartphoneAdapter already inherited from Smartphone and Socket, but by
    re-inheriting from EUSocket we redefine all the stuff inherited from Socket.
    """
    pass


class SmartphoneUSAdapter(SmartphoneAdapter, USSocket):
    """System (smartphone + adapter) for an American Socket."""
    pass


def main():

    print("Smartphone without adapter")
    smartphone = Smartphone()
    smartphone.charge(EUSocket.output_voltage)
    smartphone.charge(USSocket.output_voltage)

    print("\nSmartphone with EU adapter (object adapter approach)")
    smartphone.charge(EUAdapter.output_voltage)
    print("\nSmartphone with US adapter (object adapter approach)")
    smartphone.charge(USAdapter.output_voltage)

    print("\nSmartphone with EU adapter (class adapter approach)")
    smarthone_with_eu_adapter = SmartphoneEUAdapter()
    smarthone_with_eu_adapter.charge(EUSocket.output_voltage)
    smarthone_with_eu_adapter.charge(USSocket.output_voltage)
    print("\nSmartphone with US adapter (class adapter approach)")
    smarthone_with_us_adapter = SmartphoneUSAdapter()
    smarthone_with_us_adapter.charge(EUSocket.output_voltage)
    smarthone_with_us_adapter.charge(USSocket.output_voltage)


if __name__ == "__main__":
    main()
