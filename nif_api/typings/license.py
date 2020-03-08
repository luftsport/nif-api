from .helpers import unpack, snake_case, del_by_value, del_keys, rename_keys

"""
???
'PassiveFunctions': {
            'NewFunctionPublic': []
            }

"""


class License:
    def __init__(self, l):
        self.status, self.value = unpack(l, 'License')

        self._map()

    def _map(self):
        _del_keys = ['comment', 'person_date_of_birth', 'person_first_name', 'person_gender_id', 'person_last_name']
        keys = [('id', 'license_id'),
                ('period_from_date', 'license_period_from_date'),
                ('period_function_type_count', 'license_period_function_type_count'),
                ('period_id', 'license_period_id'),
                ('period_name', 'license_period_name'),
                ('period_owner_account_id', 'license_period_owner_account_id'),
                ('period_owner_contact_id', 'license_period_owner_contact_id'),
                ('period_owner_org_id', 'license_period_owner_org_id'),
                ('period_owner_org_name', 'license_period_owner_org_name'),
                ('period_to_date', 'license_period_to_date'),
                ('status_date', 'license_status_date'),
                ('status_id', 'license_status_id'),
                ('status_text', 'license_status_text'),
                ('type_id', 'license_type_id'),
                ('type_name', 'license_type_name'),
                ('type_price', 'license_type_price'),
                ]
        self.value = self.value['License']
        self.value = snake_case(self.value)
        self.value = del_by_value(self.value, None)
        self.value = del_keys(self.value, _del_keys)
        self.value = rename_keys(self.value, keys)
