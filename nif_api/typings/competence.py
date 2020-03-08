from .helpers import snake_case, del_by_value, rename_keys


class Competence:
    def __init__(self, competence):

        if not isinstance(competence, dict):
            raise TypeError('Not a dict')

        self.value = competence
        self._map()

    def _map(self):
        keys = [('id', 'competence_id'),
                ('sald', 'competence_sald'),
                ('title', 'competence_title'),
                ('type_id', 'competence_type_id'),
                ('additional_title', 'additional_competence_title'),
                ('approved_by_person_id', 'aprroved_by_person_id')
                ]
        self.value = snake_case(self.value)
        self.value = del_by_value(self.value, None)
        self.value = del_by_value(self.value, '')
        self.value = rename_keys(self.value, keys)

        arr = self.value['title'].split(' - ')
        try:
            if len(arr) == 2:
                # self.value['_section'] = arr[1].split('-')[0]
                self.value['_code'] = arr[0].strip()
                self.value['_name'] = arr[1].strip()
            # else:
            #    self.value['_section'] = ''
            #    self.value['_code'] = ''
            #    self.value['_name'] = ''
        except:
            pass
