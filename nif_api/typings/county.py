import typings.helpers as helpers


class County:
    def __init__(self, county):

        if not isinstance(county, dict):
            raise TypeError('Not a dict')

        self.value = county
        self._map()

    def _map(self):
        self.value = helpers.snake_case(self.value)
        self.value = helpers.del_by_value(self.value, None)
        self.value = helpers.del_by_value(self.value, '')
