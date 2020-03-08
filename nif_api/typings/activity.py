from .helpers import snake_case, del_by_value, rename_keys, del_whitelist


class Activity:
    def __init__(self, activity):
        self.value = activity

        self._map()

    def _map(self):
        keys = [('id', 'activity_id'),
                ('code', 'activity_code'),
                ('type_sa_id', 'competence_sa_id'),
                ]

        self.value = snake_case(self.value)

        try:
            self.value['code'] = int(self.value['code'])
        except:
            pass

        self.value = del_by_value(self.value, None)
        self.value = rename_keys(self.value, keys)
        self.value = del_whitelist(self.value, ['id', 'code', 'name'])
