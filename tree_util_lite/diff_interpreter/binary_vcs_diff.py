# Interpret diff for asset versioning purpose
# There must be an `interpret()` function implemented in this module

from pathlib2 import Path
from tree_util_lite.common.util import *


def interpret(diff_data, return_path=1, verbose=0):
    """Interpret diff data for binary file versioning purpose.

    Use `Node.data` to process.

    Args:
        diff_data (core.diff_engine.DiffData): abstract diff data from `core.diff_engine.DiffEngine`
            Must be in tree nodes format instead of path
    """
    data = {
        'added': [],    # Added
        'deleted': [],    # Deleted
        'renamed': {},    # Renamed
        'unchanged': [],    # Unchanged
        'modified': [],    # Modified
        'moved': {},    # Moved
    }

    # Extract file only ( any node contain data )
    for i in diff_data['insert']:
        if i.data:
            data['added'].append(i)
    for i in diff_data['delete']:
        if i.data:
            data['deleted'].append(i)
    for i in diff_data['relabel']:
        b = diff_data['relabel'][i][0]
        a = diff_data['relabel'][i][1]
        if b.data:
            if a.data == b.data:
                data['renamed'][i] = (
                    b.nice_path if return_path else b,
                    a.nice_path if return_path else a
                )
            else:
                data['added'].append(b)
                data['deleted'].append(a)
    for i in diff_data['match']:
        b = diff_data['match'][i][0]
        a = diff_data['match'][i][1]
        if b.data:
            if a.data == b.data:
                data['unchanged'].append(b.nice_path if return_path else b)
            else:
                data['modified'].append(b.nice_path if return_path else b)

    added_rem = []
    deleted_rem = []
    for b in data['added']:
        for a in data['deleted']:
            if a.label == b.label and a.data == b.data:
                data['moved'][b.nice_path] = (
                    b.nice_path if return_path else b,
                    a.nice_path if return_path else a
                )
                added_rem.append(b)
                deleted_rem.append(a)
    for i in added_rem:
        data['added'].remove(i)
    for i in deleted_rem:
        data['deleted'].remove(i)

    if return_path:
        data['added'] = [i.nice_path for i in data['added']]
        data['deleted'] = [i.nice_path for i in data['deleted']]

    if verbose:
        log_info()
        log_info('Diff data in asset versioning convention:')
        log_info(data)

    return data
