import typings.helpers as helpers


class Account:
    def __init__(self, account):

        if isinstance(account, dict):
            self.value = account
            self._map()
        else:
            self.value = {}

    def _map(self):

        self.value = helpers.snake_case(self.value)