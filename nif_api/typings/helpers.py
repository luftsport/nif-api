import inflection
from zeep.helpers import serialize_object


def unpack(obj, key, no_check=False):
    """Unpacks a zeep response object"""

    obj = dict(serialize_object(obj))

    if obj.get('Success', False) is True or no_check is True:

        return True, obj[key]

    elif obj.get('ErrorMessage', None) is not None:

        return False, {'code': obj.get('ErrorCode', 0), 'message': obj.get('ErrorMessage', '')}

    raise Exception


def _convert_keys(d, convert_function):
    """Converts keys recursively by function given"""

    if isinstance(d, dict):
        new = {}
        for k, v in d.items():
            new_v = v
            if isinstance(v, dict):
                new_v = _convert_keys(v, convert_function)
            elif isinstance(v, list):
                new_v = list()
                for x in v:
                    new_v.append(_convert_keys(x, convert_function))

            new[convert_function(k)] = new_v

        return new

    else:
        return d


def snake_case(d):
    return _convert_keys(d, inflection.underscore)


def del_keys(d, keys, del_none=False):
    """Deltes keys given in list"""
    if isinstance(d, dict):
        for k in keys:
            d.pop(k, None)

        return d
    return d

def rename_keys(d, keys):
    """Takes a list of tuples
    @todo see if all(isinstance(item, tuple) for item in keys) makes sense
    """
    if isinstance(d, dict):

        for k in keys:
            try:
                d[k[0]] = d.pop(k[1])
            except:
                pass

        return d
    return d


def del_whitelist(d, whitelist):
    """Deletes all keys not in whitelist, not recursive"""
    if isinstance(d, dict):
        keys = d.copy().keys()
        for k in keys:
            if k not in whitelist:
                d.pop(k, None)
        return d
    return d


def del_by_value(d, value=None):
    if isinstance(d, dict):
        new_d = {}
        for k, v in d.items():
            if v is not value:
                new_d.update({k: v})

        return new_d
    return d


def rename_key(d, keys):
    """Maps keys to values in dict"""
    if isinstance(d, dict):
        for k, v in keys.items():
            if k in d:
                d[v] = d[k]
                d.pop(k, None)

    return d
