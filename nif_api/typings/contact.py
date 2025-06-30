from .helpers import del_keys, del_by_value


class Contact:
    def __init__(self, contact, alternate=False):

        if alternate is True and (contact.get('alternate_address', None) is not None or contact.get('alternate_city', None) is not None or contact.get('alternate_postnumber', None) is not None):
            contact['street_address'] = contact['alternate_address']
            contact['city'] = contact['alternate_city']
            contact['zip_code'] = contact['alternate_postnumber']

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
