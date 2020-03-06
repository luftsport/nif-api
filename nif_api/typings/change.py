import typings.helpers as helpers


class Change:
    def __init__(self, change):

        if not isinstance(change, dict):
            raise TypeError('Not a dict')

        self.value = change

        self._map()

    def _map(self):

        if 'MergeResultOf' in self.value:

            if self.value['MergeResultOf'] is None:
                self.value['MergeResultOf'] = []
            elif 'int' in self.value['MergeResultOf']:
                self.value['MergeResultOf'] = self.value['MergeResultOf']['int']
            else:
                self.value['MergeResultOf'] = []

        self.value = helpers.snake_case(self.value)

        whitelist = ['change_type', 'created', 'entity_type', 'id', 'merge_result_of', 'modified',
                     'name', 'sequence_ordinal', '_ordinal', '_status', '_club_id', '_realm']

        self.value = helpers.del_whitelist(self.value, whitelist)
