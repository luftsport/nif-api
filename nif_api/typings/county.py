from .helpers import snake_case, del_by_value

class County:
    def __init__(self, county):

        if not isinstance(county, dict):
            raise TypeError('Not a dict')

        self.value = county
        self._map()

    def _map(self):
        self.value = snake_case(self.value)
        self.value = del_by_value(self.value, None)
        self.value = del_by_value(self.value, '')
