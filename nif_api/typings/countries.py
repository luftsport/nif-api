import typings.helpers as helpers
from typings.country import Country


class Countries:
    def __init__(self, countries):
        self.status, value = helpers.unpack(countries, 'Countries', True)

        if self.status is True:
            self.value = value.get('CountryPublic', [])
        else:
            self.value = []

        self._map()

    def _map(self):
        new_value = []
        for item in self.value:
            new_value.append(Country(dict(item)).value)

        self.value = new_value
