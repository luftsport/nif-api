from .helpers import unpack
from .person import Person

class Persons:
    def __init__(self, persons):

        self.status, value = unpack(persons, 'Persons')

        if self.status is True:
            self.value = value.get('PersonPublic', [])
            self._map()
        else:
            self.value = []

    def _map(self):

        new_value = []
        for item in self.value:
            new_value.append(Person(item).value)

        self.value = new_value

