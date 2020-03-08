"""
Fixes for bad NIF data
"""


def fix_organization(org, org_structure):
    try:
        if org.get('id', 0) in list(org_structure.keys()):
            org['activities'] = [org_structure[org.get('id')]]
            org['main_activity'] = org_structure[org.get('id')]

            return org
    except:
        pass

    return org
