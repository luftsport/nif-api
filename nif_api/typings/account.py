from .helpers import snake_case


class Account:
    def __init__(self, account):

        if isinstance(account, dict):
            self.value = account
            self._map()
        else:
            self.value = {}

    def _map(self):

        self.value = snake_case(self.value)