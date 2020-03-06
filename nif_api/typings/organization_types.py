import typings.helpers as helpers
from typings.organizationtype import OrganizationType


class OrganizationTypes:
    def __init__(self, organization_types):

        self.status, value = helpers.unpack(organization_types, 'OrgTypes')
        if self.status is True:
            self.value = value.get('OrgTypePublic', [])
            self._map()
        else:
            self.value = []

    def _map(self):

        new_value = []
        for item in self.value:
            new_value.append(OrganizationType(item).value)

        self.value = new_value
