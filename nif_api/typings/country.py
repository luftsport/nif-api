from .helpers import snake_case, del_by_value, rename_keys


class Country:
    def __init__(self, country):
        if not isinstance(country, dict):
            raise TypeError('Not a dict')

        self.value = country
        self._map()

    def _map(self):
        keys = [('id', 'country_id'),
                ('name', 'country_name'),
                ]
        self.value = snake_case(self.value)
        self.value = del_by_value(self.value, None)
        self.value = del_by_value(self.value, '')
        self.value = rename_keys(self.value, keys)
