from .helpers import snake_case, del_by_value, rename_keys, del_keys


class Function:
    def __init__(self, function_):
        # Only accepted from funtions
        if not isinstance(function_, dict):
            raise TypeError('Not a dict')

        self.value = function_

        self._map()

    def _map(self):
        keys = [('id', 'function_id'),
                ('type_id', 'function_type_id'),
                ('type_is_license', 'function_type_is_license'),
                ('type_name', 'function_type_name'),
                ('type_publish', 'function_type_publish')
                ]

        _del_keys = ['first_name', 'last_name']

        self.value = snake_case(self.value)
        self.value = del_by_value(self.value, None)
        self.value = rename_keys(self.value, keys)
        self.value = del_keys(self.value, _del_keys)

        self.value['org_id'] = self.value.get('active_in_org_id', 0)
