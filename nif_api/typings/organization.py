"""

    Maps a organization object
    ==========================

    NIF api obj -> Lungo api obj

"""
from .helpers import unpack, snake_case, del_by_value, del_whitelist, rename_keys
from .activities import Activities
from .activity import Activity
from .orgstructure import OrgStructure
from .contact import Contact
from .account import Account


# from typings.fixes import fix_organization


class Organization:
    def __init__(self, organization, org_structure):

        self.ORG_STRUCTURE = org_structure

        if isinstance(organization, dict) is not True and 'Org' in organization:
            status, self.value = unpack(organization, 'Org')
        else:
            self.value = organization

        # If contact then no  'contact_id'??
        self.whitelist = ['account', 'comment', 'contact', 'created', 'describing_name', 'is_active',
                          'local_council_id', 'local_council_name', 'modified', 'nif_organization_number', 'name',
                          'org_id', 'organization_type_id', 'parent_organization_id',
                          'register_authority_organization_number', 'short_name', 'activities', 'main_activity',
                          '_down', '_up']
        self._map()

    def _map(self):

        keys = [
            ('id', 'org_id'),
            ('type_id', 'organization_type_id'),
            ('parent_id', 'parent_organization_id'),
            ('authority_id', 'register_authority_organization_number')
        ]

        self.value = snake_case(self.value)

        self.value = del_by_value(self.value, None)

        self.value['contact'] = Contact(self.value.get('contact', {})).value

        if 'org_structures_down' in self.value:
            self.value['_down'] = OrgStructure(self.value['org_structures_down'], 'child').value
        else:
            self.value['_down'] = []

        if 'org_structures_up' in self.value:
            self.value['_up'] = OrgStructure(self.value['org_structures_up'], 'parent').value
        else:
            self.value['_up'] = []

        if 'activities' in self.value:
            self.value['activities'] = Activities(self.value['activities']).value
        else:
            self.value['activities'] = []

        if 'main_activity' in self.value:
            self.value['main_activity'] = Activity(self.value['main_activity']).value
        else:
            self.value['main_activity'] = {}

        if 'account' in self.value:
            self.value['account'] = Account(self.value['account']).value

        self.value = del_whitelist(self.value, self.whitelist)
        self.value = rename_keys(self.value, keys)

        # Fix all type_id = 19
        # if self.value.get('type_id', 0) == 19:
        #    self.value = fix_organization(self.value)

        if self.value['id'] in list(self.ORG_STRUCTURE.keys()):
            self.value['activities'] = [self.ORG_STRUCTURE[self.value['id']]]
            self.value['main_activity'] = self.ORG_STRUCTURE[self.value['id']]
