from .helpers import unpack
from .competence import Competence


class Competences:
    def __init__(self, competences):
        self.status, value = unpack(competences, 'Competences', True)

        if self.status is True:
            self.value = value.get('Competence', [])
        else:
            self.value = []

        self._map()

    def _map(self):
        new_value = []
        for item in self.value:
            new_value.append(Competence(dict(item)).value)

        self.value = new_value
