from .helpers import del_keys, del_by_value


class Contact:
    def __init__(self, contact):

        self.delkeys = ['name',
                        'alternate_address',
                        'alternate_city',
                        'alternate_postnumber',
                        'full_address_email_phone',
                        'full_adresse',
                        'home_address']

        if isinstance(contact, dict):
            self.value = contact
            self._map()

        else:
            self.value = {}

    def _map(self):
        self.value = del_keys(d=self.value, keys=self.delkeys)
        self.value = del_by_value(self.value, None)
