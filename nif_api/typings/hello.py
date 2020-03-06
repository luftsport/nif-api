import typings.helpers as helpers


class Hello:
    def __init__(self, hello):

        self.status, value = helpers.unpack(hello, 'HelloData')

        if self.status is True:
            self.value = value
            self._map()

    def _map(self):
        self.value = helpers.snake_case(self.value)
        self.value = helpers.del_by_value(self.value, None)
