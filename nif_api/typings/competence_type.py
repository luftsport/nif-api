from .helpers import snake_case, del_by_value, rename_keys, unpack
from xml.etree import ElementTree
import html

class CompetenceType:
    def __init__(self, competence_type):

        self.status, value = unpack(competence_type, 'CompetenceType')

        if self.status is True:
            self.value = value
            self._map()

    def remove_tags(self, text):

        try:
            text = text.strip()
        except:
            pass

        try:
            return ''.join(ElementTree.fromstring(text).itertext())
        except Exception as e:
            print('ERR', e)
            pass

        try:
            text = html.unescape(text)
        except:
            pass

        return text

    def _map(self):
        keys = [('id', 'competence_type_id'),
                ('meta_type', 'competence_meta_type'),
                ('sa_id', 'competence_sa_id'),
                ('type_sa_id', 'competence_type_sa_id'),
                ]

        self.value = snake_case(self.value)

        self.value = del_by_value(self.value, None)
        self.value = rename_keys(self.value, keys)

        self.value['description'] = self.remove_tags(self.value.get('description', ''))
        self.value['prequisites_text'] = self.remove_tags(self.value.get('prequisites_text', ''))
        self.value['title'] = self.remove_tags(self.value.get('title', ''))
