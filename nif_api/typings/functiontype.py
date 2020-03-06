import typings.helpers as helpers


class FunctionType:
    def __init__(self, function_type):
        self.value = function_type

        self._map()

    def _map(self):
        rename_keys = [('category_id', 'function_category_id'),
                       ('category_name', 'function_category_name'),
                       ('id', 'function_type_id'),
                       ('type_no', 'function_type_no')
                       ]

        self.value = helpers.snake_case(self.value)

        self.value = helpers.del_by_value(self.value, None)
        self.value = helpers.rename_keys(self.value, rename_keys)
