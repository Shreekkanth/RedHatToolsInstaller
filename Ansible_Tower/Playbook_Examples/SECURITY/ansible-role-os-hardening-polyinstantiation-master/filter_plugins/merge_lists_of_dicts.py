# From https://gist.github.com/halberom/f9c519962f163e26568d

from jinja2.utils import soft_unicode


def merge_dicts(value, dict1):
    # return a merged dict
    result = {}
    result = value
    result.update(dict1)
    return result


def merge_lists_of_dicts(list1, list2):
    # return a merged list
    result = []
    if len(list1) == len(list2):
        for index, val in enumerate(list1):
            merged_items = merge_dicts(list1[index], list2[index])
            result.append(merged_items)
    return result


class FilterModule(object):
    ''' Ansible extra jinja2 filters '''

    def filters(self):
        return {
            'merge_dicts': merge_dicts,
            'merge_lists_of_dicts': merge_lists_of_dicts
        }
