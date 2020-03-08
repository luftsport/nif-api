from .helpers import snake_case, del_by_value, rename_keys


class LicenseType:
    def __init__(self, license_type):
        if not isinstance(license_type, dict):
            raise TypeError('Not a dict')

        self.value = license_type
        self._map()

    def _map(self):
        keys = [('period_id', 'license_period_id'),
                ('id', 'license_type_id'),
                ('price', 'license_type_price'),
                ('text', 'license_type_text'),
                ]
        self.value = snake_case(self.value)
        self.value = del_by_value(self.value, None)
        self.value = del_by_value(self.value, '')
        self.value = rename_keys(self.value, keys)
