import typings.helpers as helpers

"""
???
'PassiveFunctions': {
            'NewFunctionPublic': []
            }

"""
class License:
    def __init__(self, l):

        self.status, self.value = helpers.unpack(l, 'License')

        self._map()

    def _map(self):

        del_keys = ['comment', 'person_date_of_birth', 'person_first_name', 'person_gender_id', 'person_last_name']
        rename_keys = [('id', 'license_id'),
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
        self.value = helpers.snake_case(self.value)
        self.value = helpers.del_by_value(self.value, None)
        self.value = helpers.del_keys(self.value, del_keys)
        self.value = helpers.rename_keys(self.value, rename_keys)
