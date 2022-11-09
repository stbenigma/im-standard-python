import copy
import logging
# import deepdiff

from SSOT_db.IM_JSON import JSModel

logger = logging.getLogger(__name__)


def delta_spod(lhs: JSModel, rhs: JSModel) -> dict:
    """Create a json report of the differences between left and right
    @:parameter lhs Left hand side model
    @:parameter rhs Right hand side model
    """

    ignore = set(['model', '_imprint_'])
    commons = set.union(set(lhs.jsmodel.keys()), set(rhs.jsmodel.keys())) - ignore
    #    rhk = rhs.jsmodel.keys() - ignore

    #    commons = set.intersection(lhk, rhk)
    logger.debug(f"Processing sections {commons}")

    deltas = {}
    # iterate element types
    for key in commons:
        lhv = lhs.jsmodel.get(key, {})
        rhv = rhs.jsmodel.get(key, {})
        deltas[key] = set_compare(lhv, rhv)

    result = {
        'delta': deltas,
        'inputs': {
            'lhs': copy.deepcopy(lhs.jsmodel['_imprint_']),
            'rhs': copy.deepcopy(rhs.jsmodel['_imprint_'])
        }
    }
    return result


def set_compare(lhs: dict, rhs: dict):
    """Compare two sets"""
    same = set.intersection(set(lhs.keys()), set(rhs.keys()))

    insert_set = rhs.keys() - lhs.keys()
    delete_set = lhs.keys() - rhs.keys()

    left_overlap = {key: lhs[key] for key in same}
    right_overlap = {key: rhs[key] for key in same}
    diff_set, report = content_compare(left_overlap, right_overlap)
    constant = lhs.keys() - diff_set

    result = {
        'summary': {
            'inserted': len(insert_set),
            'updated': len(diff_set),
            'deleted': len(delete_set),
            'constant': len(constant),
            'keys': {
                'inserted': list(insert_set),
                'updated': list(diff_set),
                'deleted': list(delete_set),
                'values': {
                    'inserted': {key: rhs[key] for key in insert_set},
                    'updated': report,
                },
            },
        },
    }
    return result


def content_compare(left: dict, right: dict) -> (set, dict):
    if len(left) != len(right):
        raise ValueError('Expecting same set size')

    if left.keys() != right.keys():
        raise ValueError('Expecting same keys in left and right dict')

    report = {}
    difference = set()
    for key, lvalue in left.items():
        rvalue = right[key]
        if rvalue != lvalue:
            difference.add(key)
            report[key] = diff_report(lvalue, rvalue)

    return difference, report


def diff_report(left: dict, right: dict) -> dict:
    report = {}
    for key in set(left.keys()).union(right.keys()):
        lvalue = left.get(key)
        rvalue = right.get(key)
        if lvalue != rvalue:
            report[key] = {
                'left': lvalue,
                'right': rvalue

            }
    return report
