from .helpers import unpack
from .functiontype import FunctionType


class FunctionTypes:
    def __init__(self, function_types):

        self.status, value = unpack(function_types, 'FunctionTypes')

        if self.status is True:
            self.value = value.get('FunctionTypePublic', [])
            self._map()
        else:
            self.value = []

    def _map(self):

        new_value = []
        for item in self.value:
            new_value.append(FunctionType(item).value)

        self.value = new_value
