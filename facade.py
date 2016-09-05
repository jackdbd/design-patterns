"""
With the Facade, the external system is our customer; it is better to add
complexity facing inwards if it makes the external interface simpler.
"""


# Complex parts
class _UserInterface(object):

    def __init__(self):
        print('Welcome to Big Money Bank!')
        print('Please insert your card and digit your security pin...\n')

    @staticmethod
    def display_pin_error_message():
        print('We\'re sorry, the pin you entered is wrong!\n')

    @classmethod
    def welcome_owner(cls, owner, cash):
        print('Hi {}!'.format(owner))
        print('What can we do for you?'.format(owner))
        cls.display_current_balance(cash)

    @staticmethod
    def display_transaction_successful():
        print('Transaction successful')

    @staticmethod
    def display_transaction_unsuccessful(amout):
        print('Sorry, you can\'t widraw ${}\n'.format(amout))

    @staticmethod
    def display_current_balance(cash):
        print('Your current balance is: ${}\n'.format(cash))

    @staticmethod
    def display_withdrawal(amount):
        print('Withdraw ${}'.format(amount))

    @staticmethod
    def display_deposit(amount):
        print('Deposit ${}'.format(amount))


class _AccountManager(object):

    def __init__(self):
        self._mapping = {
            '1234': {'number': 'A1b23cz567', 'owner': 'John', 'cash': 1000.0},
            '5678': {'number': 'N1b73t893y', 'owner': 'Tom', 'cash': 500.0},
        }
        self.pin = None

    @property
    def mapping(self):
        return self._mapping

    @mapping.setter
    def mapping(self, mapping):
        self._mapping = mapping

    def is_pin_valid(self, pin):
        if pin in self.mapping.keys():
            return True
        else:
            return False

    def get_account(self, pin):
        assert pin in self.mapping, 'No accounts with Pin = {}!'.format(pin)
        account = self.mapping[pin]
        return account['number'], account['owner'], account['cash']

    def get_current_cash(self):
        return self.mapping[self.pin]['cash']

    def enough_cash_in_account(self, amount_to_withdraw):
        account = self.mapping[self.pin]
        if amount_to_withdraw <= account['cash']:
            return True
        else:
            return False

    def increase_cash_in_account(self, amount_deposited):
        account = self.mapping[self.pin]
        account['cash'] += amount_deposited

    def decrease_cash_in_account(self, amount_withdrawn):
        account = self.mapping[self.pin]
        account['cash'] -= amount_withdrawn


# Facade
class ATM(object):

    def __init__(self):
        self.ui = _UserInterface()
        self.account_manager = _AccountManager()

    def digit_pin(self, pin):
        if self.account_manager.is_pin_valid(pin):
            self.account_manager.pin = pin
            account_number, owner, cash = \
                self.account_manager.get_account(pin)
            self.ui.welcome_owner(owner, cash)
        else:
            self.ui.display_pin_error_message()

    def withdraw_cash(self, amount):
        assert amount > 0, 'The amount of cash to withdraw must be positive'
        self.ui.display_withdrawal(amount)
        if self.account_manager.enough_cash_in_account(amount):
            self.account_manager.decrease_cash_in_account(amount)
            self.ui.display_transaction_successful()
            cash = self.account_manager.get_current_cash()
            self.ui.display_current_balance(cash)
        else:
            self.ui.display_transaction_unsuccessful(amount)

    def deposit_cash(self, amount):
        assert amount > 0, 'The amount of cash to deposit must be positive'
        self.ui.display_deposit(amount)
        self.account_manager.increase_cash_in_account(amount)
        self.ui.display_transaction_successful()
        cash = self.account_manager.get_current_cash()
        self.ui.display_current_balance(cash)


def main():
    atm = ATM()
    atm.digit_pin('1234')
    atm.withdraw_cash(500.0)
    atm.withdraw_cash(600.0)
    atm.deposit_cash(200.0)
    atm.withdraw_cash(600.0)

if __name__ == '__main__':
    main()
