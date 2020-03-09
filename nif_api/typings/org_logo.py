from .helpers import unpack

class OrgLogo:
    def __init__(self, org_logo):
        self.status, value = unpack(org_logo, 'OrgLogo', True)

        if self.status is True:
            self.value = value.get('Data', b'')
        else:
            self.value = b''

        # self._map()

    def _map(self):
        pass

