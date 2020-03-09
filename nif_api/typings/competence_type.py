from .helpers import snake_case, del_by_value, rename_keys


class CompetenceType:
    def __init__(self, competence_type):
        self.value = competence_type

        self._map()

    def _map(self):
        keys = [('id', 'competence_type_id'),
                       ('meta_type', 'competence_meta_type'),
                       ('type_sa_id', 'competence_sa_id'),
                       ]

        self.value = snake_case(self.value)

        self.value = del_by_value(self.value, None)
        self.value = rename_keys(self.value, keys)
