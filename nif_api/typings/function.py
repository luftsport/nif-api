import typings.helpers as helpers


class Function:
    def __init__(self, function_):
        # Only accepted from funtions
        if not isinstance(function_, dict):
            raise TypeError('Not a dict')

        self.value = function_

        self._map()

    def _map(self):
        rename_keys = [('id', 'function_id'),
                       ('type_id', 'function_type_id'),
                       ('type_is_license', 'function_type_is_license'),
                       ('type_name', 'function_type_name'),
                       ('type_publish', 'function_type_publish')
                       ]

        del_keys = ['first_name', 'last_name']

        self.value = helpers.snake_case(self.value)
        self.value = helpers.del_by_value(self.value, None)
        self.value = helpers.rename_keys(self.value, rename_keys)
        self.value = helpers.del_keys(self.value, del_keys)

        self.value['org_id'] = self.value.get('active_in_org_id', 0)
