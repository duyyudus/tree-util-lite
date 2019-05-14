# ABSTRACT:
#
# There are 4 steps in tree diff computation
#   1. Compute tree distance using one of algorithms in `tree_distance`
#   2. Compute edit sequence from tree distance matrix
#   3. Postprocess edit sequence to raw diff data `DiffData`
#   4. Interpret raw diff data using one of interpreters in `diff_interpreter`
#       There is one built-in interpreter `binary_vcs_diff`, used for binary file versioning system

from tree_util_lite.common.util import *
from tree_util_lite.tree_distance import zhang_shasha, descendant_alignment


class TreeDistAlgo(object):
    ZHANG_SHASHA = 'ZHANG_SHASHA'
    DESCENDANT_ALIGNMENT = 'DESCENDANT_ALIGNMENT'


class DiffData(dict):
    """Store node path with raw diff types.

    This data can be interpreted in some way, depend on purpose
    Please look at `diff_interpreter` package

    Raw diff types:
        'insert': [list str or Node]
        'delete': [list str or Node]
        'relabel': {nice_path: ( str or Node of old tree T1, str or Node of new tree T2 )}
        'match': {nice_path: ( str or Node of old tree T1, str or Node of new tree T2 )}

    """

    def __init__(self):
        super(DiffData, self).__init__()
        self['insert'] = []
        self['delete'] = []
        self['relabel'] = {}
        self['match'] = {}


class DiffEngine(object):
    """Compare difference between 2 trees using tree-edit-distance algorithms.

    Individual tree-edit-distance algorithms are implemented in `tree_util_lite.tree_distance`

    Attributes:
        _tree1 (tree.Tree):
        _tree2 (tree.Tree):
        _tree_distance (tree_distance.TreeDistance):
        _edit_sequence (list of 2-tuple):
        _diff_data (DiffData):

    Properties:
        diff_data (DiffData):

    Methods:
        compute_edit_sequence
        render_edit_sequence
        postprocess_edit_sequence

    """

    def __init__(self, tree1, tree2,
                 tree_distance_algo=TreeDistAlgo.DESCENDANT_ALIGNMENT,
                 del_cost=1,
                 ins_cost=1,
                 rel_cost=1):
        """
        Args:
            tree1 (tree.Tree):
            tree2 (tree.Tree):
        """

        super(DiffEngine, self).__init__()
        self._tree1 = tree1
        self._tree2 = tree2
        if tree_distance_algo == TreeDistAlgo.ZHANG_SHASHA:
            self._tree_distance = zhang_shasha.ZhangShasha(
                tree1.root,
                tree2.root,
                del_cost,
                ins_cost,
                rel_cost
            )
        elif tree_distance_algo == TreeDistAlgo.DESCENDANT_ALIGNMENT:
            self._tree_distance = descendant_alignment.DescendantAlignment(
                tree1.root,
                tree2.root,
                del_cost,
                ins_cost,
                rel_cost
            )
        else:
            raise Exception('Please choose a tree distance algorithm')
        self._edit_sequence = None
        self._diff_data = None

    @property
    def diff_data(self):
        """DiffData: access `self._diff_data` without recomputing postprocess edit sequence."""
        return self._diff_data

    def compute_edit_sequence(self, show_matrix=0, show_edit=0, verbose=0):
        """Raw edit sequence, in form of a list of 2-tuple.

        Tree distance matrix will be also computed here if not yet.

        Atomic edit operation:
            delete
            insert
            relabel

        Each tuple is a mapping, in 3 types:
            (node_in_tree1, node_in_tree2): relabel edit operation
            (node_in_tree1, None): delete edit operation
            (None, node_in_tree2): insert edit operation

        Args:
            show_matrix (bool): show distance matrix with backtrack path in console
            show_edit (bool): show edit sequence in console

        """
        if self._tree_distance._TD[0][0] is None:
            self._tree_distance.compute_tree_distance(verbose=verbose)
        self._edit_sequence = self._tree_distance.compute_edit_sequence(show_matrix=show_matrix)

        if show_edit:
            self.render_edit_sequence()

    def render_edit_sequence(self):
        print('')
        print('Edit sequence:')
        print('')
        size = max([len(p[0].nice_path) if p[0] else 0 for p in self._edit_sequence])
        for p in self._edit_sequence:
            label_1 = p[0].label if p[0] else '__'
            label_2 = p[1].label if p[1] else '__'
            path_1 = p[0].nice_path if p[0] else '__'
            path_2 = p[1].nice_path if p[1] else '__'
            tail_1 = ' ' * (size - len(path_1))
            if label_1 == '__':
                mapping = '--insert--->'
            elif label_2 == '__':
                mapping = '--delete--->'
            elif label_1 == label_2:
                mapping = '----------->'
            else:
                mapping = '--relabel-->'
            print(
                '  {}{}'.format(path_1, tail_1),
                mapping,
                path_2
            )

    def postprocess_edit_sequence(self,
                                  tree_distance_algo=TreeDistAlgo.DESCENDANT_ALIGNMENT,
                                  return_path=1,
                                  show_diff=0):
        """Process raw edit sequence to get a more compact diff data.

        Use edit sequence itself and `Node.nice_path` to process.
        Edit sequence from different tree distance algorithms will need its own way of postprocessing.

        Args:
            tree_distance_algo (TreeDistAlgo): process edit sequence generated from a specific tree distance algo
                By default, it is `TreeDistAlgo.DESCENDANT_ALIGNMENT`

        Returns:
            DiffData:
        """
        diff = DiffData()

        if tree_distance_algo == TreeDistAlgo.DESCENDANT_ALIGNMENT:
            for a, b in self._edit_sequence:
                if a and not b:
                    diff['delete'].append(a.nice_path if return_path else a)
                elif not a and b:
                    diff['insert'].append(b.nice_path if return_path else b)
                elif a and b and a.label != b.label:
                    if a.parent.nice_path == b.parent.nice_path:
                        diff['relabel'][b.nice_path] = (a.nice_path, b.nice_path) if return_path else (a, b)
                    else:
                        diff['insert'].append(b.nice_path if return_path else b)
                        diff['delete'].append(a.nice_path if return_path else a)
                elif a and b:
                    if a.nice_path == b.nice_path:
                        diff['match'][b.nice_path] = (a.nice_path, b.nice_path) if return_path else (a, b)
                    else:
                        diff['insert'].append(b.nice_path if return_path else b)
                        diff['delete'].append(a.nice_path if return_path else a)

        if show_diff:
            print('')
            log_info('Raw diff data below:')
            log_info(diff)

        self._diff_data = diff
        return self._diff_data
