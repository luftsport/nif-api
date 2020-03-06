import typings.helpers as helpers


class OrganizationType:
    def __init__(self, organization_type):
        self.value = organization_type

        self._map()

    def _map(self):
        self.value = helpers.snake_case(self.value)
        self.value = helpers.del_by_value(self.value, None)
