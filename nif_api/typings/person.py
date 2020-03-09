from .contact import Contact
from .gender import Gender
from .clubs import Clubs
from .helpers import unpack, snake_case, del_by_value, del_keys, rename_key
from datetime import datetime, date


class Person:
    def __init__(self, person):

        if 'Success' in person:
            self.value = unpack(person, 'PersonPublic')

        else:
            self.value = person

        self._map()

    def _map(self):
        """Should have a list of keys to delete or to fix if None"""

        keys = ['extra_addresses', 'id', 'my_profile_settings',
                'active_clubs', 'qualifications',
                'active_functions', 'function_applications', 'passive_functions']

        # Convert to snake case
        self.value = snake_case(self.value)

        # Now delete None values
        self.value = del_by_value(self.value, None)
        self.value = del_keys(self.value, keys)

        # Rename keys
        self.value = rename_key(self.value, {'person_id': 'id',
                                             'person_gender': 'gender',
                                             'home_address': 'address'})

        self.value['address'] = Contact(self.value['address']).value
        self.value['gender'] = Gender(self.value['gender']).value

        # Fix email
        if len(self.value['address'].get('email', '').strip()) > 2:
            self.value['address']['email'] = self.value['address'].get('email', '').split(';')
        elif self.value['address'].get('email', None) is not None:
            self.value.pop('email', None)

        # Fix datetime if problems (1-1-1-0-0)
        if isinstance(self.value.get('birth_date', None), datetime) is False or \
                datetime.combine(datetime.min.date(), datetime.min.time()) == self.value.get('birth_date', None):
            self.value.pop('birth_date', None)
        elif isinstance(self.value.get('birth_date', None), date) is True:
            self.value['birth_date'] = datetime.combine(self.value['birth_date'], datetime.min.time())

        # Shuffle and delete
        self.value['settings'] = {}
        self.value['settings'].update({'restricted_address': self.value.get('restricted_address', False)})
        self.value['settings'].update({'is_validated': self.value.get('is_validated', False)})
        self.value['settings'].update({'is_person_info_locked': self.value.get('is_person_info_locked', False)})
        self.value['settings'].update(
            {'automatic_data_cleansing_reservation': self.value.get('automatic_data_cleansing_reservation', False)})
        self.value['settings'].update({'approve_publishing': self.value.get('approve_publishing', False)})
        self.value['settings'].update({'approve_marketing': self.value.get('approve_marketing', False)})

        self.value = del_keys(self.value, ['restricted_address', 'is_validated', 'is_person_info_locked',
                                           'automatic_data_cleansing_reservation', 'approve_publishing',
                                           'approve_marketing'])

        # self.value = dict((self.mapping.get(k, k), v) for (k, v) in self.value.items())
        # @TODO Address email split on ;
        # self.value['address']['email'] = self.value['address']['email'].split(';')

        # New empty fields/placeholders
        # self.value['active_clubs'] = Clubs(self.value['active_clubs']).value
        self.value['clubs'] = []  # Clubs(self.value.get('clubs', [])).value
        self.value['functions'] = []  # self.value.get('functions', {}).get('function_public', [])
        # self.value['qualifications'] = self.value['qualifications']['qualification']

        self.value['competences'] = []
        self.value['licenses'] = []
