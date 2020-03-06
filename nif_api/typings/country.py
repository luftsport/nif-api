import typings.helpers as helpers


class Country:
    def __init__(self, country):

        if not isinstance(country, dict):
            raise TypeError('Not a dict')

        self.value = country
        self._map()

    def _map(self):
        rename_keys = [('id', 'country_id'),
                       ('name', 'country_name'),
                       ]
        self.value = helpers.snake_case(self.value)
        self.value = helpers.del_by_value(self.value, None)
        self.value = helpers.del_by_value(self.value, '')
        self.value = helpers.rename_keys(self.value, rename_keys)
