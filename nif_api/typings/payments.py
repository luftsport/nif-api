from .helpers import unpack
from .payment import Payment


class Payments:
    def __init__(self, payments):
        self.status, value = unpack(payments, 'PaymentDetails')

        if self.status is True:
            self.value = value.get('PaymentDetails', [])
            print(self.status, self.value)
            self._map()
        else:
            self.value = []

    def _map(self):

        new_value = []
        for item in self.value:
            new_value.append(Payment(item).value)

        self.value = new_value
