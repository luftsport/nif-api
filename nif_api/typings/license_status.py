from .helpers import snake_case, del_by_value, rename_keys

class LicenseStatus:
    def __init__(self, license_status):

        if not isinstance(license_status, dict):
            raise TypeError('Not a dict')

        self.value = license_status
        self._map()

    def _map(self):
        keys = [('id', 'license_status_id')]
        self.value = snake_case(self.value)
        self.value = del_by_value(self.value, None)
        self.value = del_by_value(self.value, '')
        self.value = rename_keys(self.value, keys)
