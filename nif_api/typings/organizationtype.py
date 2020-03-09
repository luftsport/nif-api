from .helpers import snake_case, del_by_value

class OrganizationType:
    def __init__(self, organization_type):
        self.value = organization_type

        self._map()

    def _map(self):
        self.value = snake_case(self.value)
        self.value = del_by_value(self.value, None)
