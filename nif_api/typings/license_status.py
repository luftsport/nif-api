import typings.helpers as helpers


class LicenseStatus:
    def __init__(self, license_status):

        if not isinstance(license_status, dict):
            raise TypeError('Not a dict')

        self.value = license_status
        self._map()

    def _map(self):
        rename_keys = [('id', 'license_status_id')]
        self.value = helpers.snake_case(self.value)
        self.value = helpers.del_by_value(self.value, None)
        self.value = helpers.del_by_value(self.value, '')
        self.value = helpers.rename_keys(self.value, rename_keys)
