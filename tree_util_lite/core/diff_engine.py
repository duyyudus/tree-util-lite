from tree_util_lite.common.util import *
from tree_util_lite.tree_distance import zhang_shasha


class TreeDistAlgo(object):
    ZHANG_SHASHA = 'ZHANG_SHASHA'


class DiffData(dict):

    def __init__(self):
        super(DiffData, self).__init__()


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
        postprocess_edit_sequence
        interpret_diff

    """

    def __init__(self, tree1, tree2, tree_distance_algo=TreeDistAlgo.ZHANG_SHASHA):
        """
        Args:
            tree1 (tree.Tree):
            tree2 (tree.Tree):
        """

        super(DiffEngine, self).__init__()
        self._tree1 = tree1
        self._tree2 = tree2
        if tree_distance_algo == TreeDistAlgo.ZHANG_SHASHA:
            self._tree_distance = zhang_shasha.ZhangShasha(tree1.root, tree2.root)
        else:
            raise Exception('Please choose a tree distance algorithm')
        self._edit_sequence = None
        self._diff_data = None

    @property
    def diff_data(self):
        """DiffData: """
        return self._diff_data

    def compute_edit_sequence(self):
        """Raw edit sequence, in form of a list of 2-tuple.

        Atomic edit operation:
            delete
            insert
            relabel

        Each tuple is a mapping, in 3 types:
            (node_in_tree1, node_in_tree2): relabel edit operation
            (node_in_tree1, None): delete edit operation
            (None, node_in_tree2): insert edit operation

        """
        self._edit_sequence = self._tree_distance.compute_edit_sequence()

    def postprocess_edit_sequence(self):
        """Process raw edit sequence to get a more compact diff data.

        Returns:
            DiffData:
        """
        self._diff_data = DiffData()
        return self.diff_data

    def interpret_diff(self):
        """Interpret diff data in some way, depend on purpose.

        Returns:
            dict: interpreted diff data
        """
        return {}
