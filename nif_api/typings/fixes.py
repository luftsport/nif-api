"""
Fixes for bad NIF data
"""
from settings import NLF_ORG_STRUCTURE

def fix_organization(org):

    try:
        if org.get('id', 0) in list(NLF_ORG_STRUCTURE.keys()):

            org['activities'] = [NLF_ORG_STRUCTURE[org.get('id')]]
            org['main_activity'] = NLF_ORG_STRUCTURE[org.get('id')]

            return org
    except:
        pass

    return org
