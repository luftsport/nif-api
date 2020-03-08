from .helpers import unpack
from .organization import Organization


class Organizations:
    def __init__(self, organizations, org_structure):
        self.ORG_STRUCTURE = org_structure
        self.status, value = unpack(organizations, 'Orgs')

        if self.status is True:
            self.value = value.get('OrgPublic', [])
            self._map()
        else:
            self.value = []

    def _map(self):

        new_value = []
        for item in self.value:
            new_value.append(Organization(item, self.ORG_STRUCTURE).value)

        self.value = new_value
