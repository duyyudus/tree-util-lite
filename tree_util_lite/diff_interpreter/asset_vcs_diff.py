# Interpret diff for asset versioning purpose
# There must be an `interpret()` function implemented in this module

from pathlib2 import Path
from tree_util_lite.common.util import *


def interpret(diff_data, return_path=1, verbose=0):
    """
    Args:
        diff_data (core.diff_engine.DiffData): abstract diff data from `core.diff_engine.DiffEngine`
            Must be in tree nodes format instead of path
    """
    data = {
        'A': [],    # Added
        'D': [],    # Deleted
        'R': {},    # Renamed
        'U': [],    # Unchanged
        'M': [],    # Modified
    }

    # Extract file only
    for i in diff_data['insert']:
        if '.' in Path(i.nice_path).name:
            data['A'].append(i.nice_path if return_path else i)
    for i in diff_data['delete']:
        if '.' in Path(i.nice_path).name:
            data['D'].append(i.nice_path if return_path else i)
    for i in diff_data['relabel']:
        if '.' in Path(i).name:
            b = diff_data['relabel'][i][0]
            a = diff_data['relabel'][i][1]
            data['R'][i] = (
                b.nice_path if return_path else i,
                a.nice_path if return_path else i,
            )
    for i in diff_data['match']:
        if '.' in Path(i).name:
            b = diff_data['match'][i][0]
            a = diff_data['match'][i][1]
            if a.data == b.data:
                data['U'].append(b.nice_path if return_path else i)
            else:
                data['M'].append(b.nice_path if return_path else i)

    if verbose:
        log_info()
        log_info('Diff data in asset versioning convention:')
        log_info(data)

    return data
