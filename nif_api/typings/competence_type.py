from .helpers import snake_case, del_by_value, rename_keys, unpack, del_whitelist
from xml.etree import ElementTree
import html


class CompetenceType:
    def __init__(self, competence_type):

        self.status, value = unpack(competence_type, 'CompetenceType')

        if self.status is True:
            self.value = value
            self._map()

    def _remove_tags(self, text):

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
                ('attributes', 'custom_attributes')
                ]

        self.value = snake_case(self.value)

        self.value = del_by_value(self.value, None)
        self.value = rename_keys(self.value, keys)

        whitelist = ['attributes',
                     'categories',
                     'checked_by',
                     'children',
                     'code',
                     'colorcode',
                     'id',
                     'meta_type',
                     'type_id',
                     'type_sa_id',
                     'description',
                     'duration',
                     'durations',
                     'files',
                     'instructors',
                     'languages_available',
                     'locale',
                     'max_age',
                     'min_age',
                     'modified',
                     'organisations',
                     'pre_requisites',
                     'prequisites_text',
                     'short_description',
                     'sports',
                     'title',
                     'valid_for',
                     'weight']

        self.value = del_whitelist(self.value, whitelist)
        CompetenceType
        self.value['description'] = self._remove_tags(self.value.get('description', ''))
        self.value['prequisites_text'] = self._remove_tags(self.value.get('prequisites_text', ''))
        self.value['title'] = self._remove_tags(self.value.get('title', ''))
        self.value['colorcode'] = self._remove_tags(self.value.get('colorcode', ''))

        # Remove xml type
        self.value['children'] = self.value.get('children', {}).get('competence_type', [])
        self.value['pre_requisites'] = self.value.get('pre_requisites', {}).get('competence_type', [])
        self.value['sports'] = self.value.get('sports', {}).get('sport_simple', [])
        self.value['organisations'] = self.value.get('organisations', {}).get('organisation', [])
        self.value['languages_available'] = self.value.get('languages_available', {}).get('string', [])
        self.value['durations'] = self.value.get('durations', {}).get('duration', [])
        self.value['categories'] = self.value.get('categories', {}).get('course_category', [])
        self.value['instructors'] = self.value.get('instructors', {}).get('Person', [])
