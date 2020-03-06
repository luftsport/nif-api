"""

    Maps a organization object
    ==========================

    NIF api obj -> Lungo api obj

"""
import typings.helpers as helpers

from typings.activities import Activities
from typings.activity import Activity
from typings.orgstructure import OrgStructure
from typings.contact import Contact
from typings.account import Account
# from typings.fixes import fix_organization
from settings import NLF_ORG_STRUCTURE


class Organization:
    def __init__(self, organization):

        if isinstance(organization, dict) is not True and 'Org' in organization:
            status, self.value = helpers.unpack(organization, 'Org')
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

        rename_keys = [
            ('id', 'org_id'),
            ('type_id', 'organization_type_id'),
            ('parent_id', 'parent_organization_id'),
            ('authority_id', 'register_authority_organization_number')
        ]

        self.value = helpers.snake_case(self.value)

        self.value = helpers.del_by_value(self.value, None)

        self.value['contact'] = Contact(self.value['contact']).value

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

        self.value = helpers.del_whitelist(self.value, self.whitelist)
        self.value = helpers.rename_keys(self.value, rename_keys)

        # Fix all type_id = 19
        # if self.value.get('type_id', 0) == 19:
        #    self.value = fix_organization(self.value)

        if self.value['id'] in list(NLF_ORG_STRUCTURE.keys()):
            self.value['activities'] = [NLF_ORG_STRUCTURE[self.value['id']]]
            self.value['main_activity'] = NLF_ORG_STRUCTURE[self.value['id']]
