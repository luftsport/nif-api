import typings.helpers as helpers


class CompetenceType:
    def __init__(self, competence_type):
        self.value = competence_type

        self._map()

    def _map(self):
        rename_keys = [('id', 'competence_type_id'),
                       ('meta_type', 'competence_meta_type'),
                       ('type_sa_id', 'competence_sa_id'),
                       ]

        self.value = helpers.snake_case(self.value)

        self.value = helpers.del_by_value(self.value, None)
        self.value = helpers.rename_keys(self.value, rename_keys)