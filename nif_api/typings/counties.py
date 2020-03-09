from .helpers import unpack
from .county import County


class Counties:
    def __init__(self, counties):
        self.status, value = unpack(counties, 'Regions', True)

        if self.status is True:
            self.value = value.get('RegionPublic', [])
        else:
            self.value = []

        self._map()

    def _map(self):
        new_value = []
        for item in self.value:
            new_value.append(County(dict(item)).value)

        self.value = new_value
