import typings.helpers as helpers


class Activity:
    def __init__(self, activity):
        self.value = activity

        self._map()

    def _map(self):
        rename_keys = [('id', 'activity_id'),
                       ('code', 'activity_code'),
                       ('type_sa_id', 'competence_sa_id'),
                       ]

        self.value = helpers.snake_case(self.value)

        try:
            self.value['code'] = int(self.value['code'])
        except:
            pass

        self.value = helpers.del_by_value(self.value, None)
        self.value = helpers.rename_keys(self.value, rename_keys)
        self.value = helpers.del_whitelist(self.value, ['id', 'code', 'name'])
