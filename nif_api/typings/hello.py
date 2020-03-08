from .helpers import unpack, snake_case, del_by_value

class Hello:
    def __init__(self, hello):

        self.status, value = unpack(hello, 'HelloData')

        if self.status is True:
            self.value = value
            self._map()

    def _map(self):
        self.value = snake_case(self.value)
        self.value = del_by_value(self.value, None)
