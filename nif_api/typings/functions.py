import typings.helpers as helpers
from typings.function import Function


class Functions:
    def __init__(self, functions):

        self.status, value = helpers.unpack(functions, 'Functions')

        if self.status is True:
            self.value = value.get('FunctionPublic', [])
            self._map()
        else:
            self.value = []

    def _map(self):

        new_value = []
        for item in self.value:
            new_value.append(Function(item).value)

        self.value = new_value


