from .helpers import unpack
from .license_status import LicenseStatus


class LicensesStatus:
    def __init__(self, licenses_status):
        self.status, value = unpack(licenses_status, 'LicenseStatuses', True)

        if self.status is True:
            self.value = value.get('LicenseStatusPublic', [])
        else:
            self.value = []

        self._map()

    def _map(self):
        new_value = []
        for item in self.value:
            new_value.append(LicenseStatus(dict(item)).value)

        self.value = new_value
