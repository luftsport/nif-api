import typings.helpers as helpers
from typings.change import Change

class Changes:

    def __init__(self, changes):

        self.status, value = helpers.unpack(changes, 'Synchronization')

        if self.status is True and 'Changes' in value and value['Changes'] is not None:
            self.value = value['Changes'].get('ChangeInfo', [])
            self._map()
        else:
            self.value = []

    def _map(self):

        new_value = []
        for item in self.value:
            new_value.append(Change(item).value)

        self.value = new_value
