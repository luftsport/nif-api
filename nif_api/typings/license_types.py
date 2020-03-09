from .helpers import unpack
from .license_type import LicenseType


class LicenseTypes:
    def __init__(self, license_types):
        self.status, value = unpack(license_types, 'LicenseTypes', True)

        if self.status is True:
            self.value = value.get('LicenseTypePublic', [])
        else:
            self.value = []

        self._map()

    def _map(self):
        new_value = []
        for item in self.value:
            new_value.append(LicenseType(dict(item)).value)

        self.value = new_value
