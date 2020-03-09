from .helpers import snake_case

class OrgStructure:
    def __init__(self, organization, direction):

        self.direction = direction

        if 'OrgStructurePublic' in organization:
            self.value = organization['OrgStructurePublic']
            self._map()
        elif 'org_structure_public' in organization:
            self.value = organization['org_structure_public']
            self._map()
        elif isinstance(organization, dict):
            self.value = organization
            self._map()
        else:
            self.value = []

    def _map(self):

        new_value = []
        for row in self.value:
            row = snake_case(row)

            # if row['org_id_{}'.format(self.direction)] not in self.disallow_ids and row[
            #        'org_type_id_{}'.format(self.direction)] not in self.disallow_types:

            new_value.append({'id': row['org_id_{}'.format(self.direction)],
                              'type': row['org_type_id_{}'.format(self.direction)]})
        self.value = new_value
