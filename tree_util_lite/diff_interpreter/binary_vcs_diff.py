# Interpret diff for asset versioning purpose
# There must be an `interpret()` function implemented in this module

from tree_util_lite.common.util import *


def interpret(diff_data, return_path=1, show_diff=0):
    """Interpret diff data for binary file versioning purpose.

    Use `Node.data` as file hash digest to process only nodes contain data.
    All paths are converted to relative format ( without root )

    Args:
        diff_data (core.diff_engine.DiffData): raw diff data from `core.diff_engine.DiffEngine`
            Must be in tree nodes format instead of path
    Returns:
        dict: interpreted diff data, in following format:
            {
                'added': list,  # Added
                'deleted': list,  # Deleted
                'renamed': dict,  # Renamed: same parent, different label, same hash
                'unchanged': list,  # Unchanged: same parent, same label, same hash
                'modified': list,  # Modified: same parent, same label, different hash
                'moved': dict,  # Moved: different parent, same label, same hash
                'copied': dict,  # Copied: any node share hash with some node in `unchanged`
            }
    """
    data = {
        'added': [],
        'deleted': [],
        'renamed': {},
        'unchanged': [],
        'modified': [],
        'moved': {},
        'copied': {},
    }

    # Extract `added` and `deleted`
    for i in diff_data['insert']:
        if i.data:
            data['added'].append(i)
    for i in diff_data['delete']:
        if i.data:
            data['deleted'].append(i)

    # Extract `renamed`
    for i in diff_data['relabel']:
        a = diff_data['relabel'][i][0]
        b = diff_data['relabel'][i][1]
        if b.data:
            if a.data == b.data:
                data['renamed'][i] = (
                    a.nice_relative_path if return_path else a,
                    b.nice_relative_path if return_path else b
                )
            else:
                data['added'].append(b)
                data['deleted'].append(a)

    # Extract `unchanged` and `modified`
    for i in diff_data['match']:
        a = diff_data['match'][i][0]
        b = diff_data['match'][i][1]
        if b.data:
            if a.data == b.data:
                data['unchanged'].append(b)
            else:
                data['modified'].append(b.nice_relative_path if return_path else b)

    # Final extract `moved`, `unchanged`, `modified`, `renamed` from `added` and `deleted` node pairs
    added_rem = []
    deleted_rem = []
    for b in data['added']:
        for a in data['deleted']:
            if a.nice_relative_path == b.nice_relative_path and a.data == b.data:
                data['unchanged'].append(b)
                added_rem.append(b)
                deleted_rem.append(a)
            elif a.nice_relative_path == b.nice_relative_path and a.data != b.data:
                data['modified'].append(b.nice_relative_path if return_path else b)
                added_rem.append(b)
                deleted_rem.append(a)
            elif a.label == b.label and a.data == b.data:
                data['moved'][b.nice_relative_path] = (
                    a.nice_relative_path if return_path else a,
                    b.nice_relative_path if return_path else b
                )
                added_rem.append(b)
                deleted_rem.append(a)
            elif a.parent.nice_relative_path == b.parent.nice_relative_path and a.data == b.data:
                data['renamed'][b.nice_relative_path] = (
                    a.nice_relative_path if return_path else a,
                    b.nice_relative_path if return_path else b
                )
                added_rem.append(b)
                deleted_rem.append(a)
    for i in added_rem:
        data['added'].remove(i)
    for i in deleted_rem:
        data['deleted'].remove(i)

    # Extract `copied`
    added_rem = []
    for b2 in data['added']:
        for b1 in data['unchanged']:
            if b1.data == b2.data:
                data['copied'][b2.nice_relative_path] = (
                    b1.nice_relative_path if return_path else b1,
                    b2.nice_relative_path if return_path else b2
                )
                added_rem.append(b2)
    for i in added_rem:
        data['added'].remove(i)

    if return_path:
        data['added'] = [i.nice_relative_path for i in data['added']]
        data['deleted'] = [i.nice_relative_path for i in data['deleted']]
        data['unchanged'] = [i.nice_relative_path for i in data['unchanged']]

    if show_diff:
        print('')
        log_info('Diff data in binary file versioning convention:')
        log_info(data)

    return data
