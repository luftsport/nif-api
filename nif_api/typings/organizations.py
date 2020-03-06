import typings.helpers as helpers
from typings.organization import Organization


class Organizations:
    def __init__(self, organizations):

        self.status, value = helpers.unpack(organizations, 'Orgs')

        if self.status is True:
            self.value = value.get('OrgPublic', [])
            self._map()
        else:
            self.value = []

    def _map(self):

        new_value = []
        for item in self.value:
            new_value.append(Organization(item).value)

        self.value = new_value
