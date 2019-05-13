# Zhang Shasha tree edit distance algorithm

from tree_util_lite.common.util import *
from . import TreeDistance


class DescendantAlignment(TreeDistance):
    """Simple descendant alignment algo

    Inherit from `TreeDistance`

    Attributes:
        _r1 (core.tree.Node):
        _r2 (core.tree.Node):
        _T1 (list of core.tree.Node):
        _T2 (list of core.tree.Node):
        _L1 (tuple of int):
        _L2 (tuple of int):
        _KR1 (tuple of int):
        _KR2 (tuple of int):
        _TD (list of list of int):
        _del_cost (int):
        _ins_cost (int):
        _rel_cost (int):

    Properties:
        r1 (core.tree.Node):
        r2 (core.tree.Node):
        TD (tuple of tuple of int): immutable version of self._TD

    Methods:
        set_del_cost
        set_ins_cost
        set_rel_cost
    """

    def __init__(self, r1, r2, del_cost=1, ins_cost=1, rel_cost=1):
        """
        Args:
            r1 (core.tree.Node): root of tree 1
            r2 (core.tree.Node): root of tree 2
            del_cost (int): cost of delete edit operation
            ins_cost (int): cost of insert edit operation
            rel_cost (int): cost of relabel edit operation
        """
        super(DescendantAlignment, self).__init__(r1, r2, del_cost, ins_cost, rel_cost)

        self._T1 = tuple([None] + list(self._r1.nodes_by_preorder))
        self._T2 = tuple([None] + list(self._r2.nodes_by_preorder))

    def compute_tree_distance(self, verbose=0):
        """Compute matrix `self._TD`."""

        TD = self._TD
        TD[0][0] = 0

        for i in range(1, len(TD)):
            TD[i][0] = TD[i - 1][0] + self._del_cost
        for j in range(1, len(TD[0])):
            TD[0][j] = TD[0][j - 1] + self._ins_cost

        for i in range(1, len(self._T1)):
            for j in range(1, len(self._T2)):
                TD[i][j] = min(
                    TD[i - 1][j] + self._del_cost,
                    TD[i][j - 1] + self._ins_cost,
                    TD[i - 1][j - 1] + (self._rel_cost if self._T1[i].label != self._T2[j].label else 0)
                )
                if verbose:
                    log_info('Updated value at T1[{}] -> T2[{}]'.format(i, j))
