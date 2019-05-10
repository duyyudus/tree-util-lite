# Zhang Shasha tree edit distance algorithm

from tree_util_lite.common.util import *
from . import TreeDistance


class ZhangShasha(TreeDistance):
    """Zhang Shasha algo

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
        super(ZhangShasha, self).__init__(r1, r2, del_cost, ins_cost, rel_cost)

    def _forest_dist(self, i, j, L1, L2, TD, verbose):
        if verbose:
            log_info('Compute distance between subtree pair at keyroot: T1[{}] -> T2[{}]'.format(i, j))

        # Temporary forest distance matrix
        FD = [[None for col in range(len(self._T2))] for row in range(len(self._T1))]
        FD[0][0] = 0

        # Starting cell
        FD[L1[i] - 1][L2[j] - 1] = 0

        for di in range(L1[i], i + 1):
            FD[di][L2[j] - 1] = FD[di - 1][L2[j] - 1] + self._del_cost

        for dj in range(L2[j], j + 1):
            FD[L1[i] - 1][dj] = FD[L1[i] - 1][dj - 1] + self._ins_cost

        for di in range(L1[i], i + 1):
            for dj in range(L2[j], j + 1):
                if L1[di] == L1[i] and L2[dj] == L2[j]:
                    FD[di][dj] = min(
                        FD[di - 1][dj] + self._del_cost,
                        FD[di][dj - 1] + self._ins_cost,
                        FD[di - 1][dj - 1] + (self._rel_cost if self._T1[di].label != self._T2[dj].label else 0)
                    )
                    TD[di][dj] = FD[di][dj]
                    if verbose:
                        log_info('----Updated subtree distance T1[{}] -> T2[{}] with value: {}'.format(
                            di, dj, TD[di][dj]
                        ))
                else:
                    FD[di][dj] = min(
                        FD[di - 1][dj] + self._del_cost,
                        FD[di][dj - 1] + self._ins_cost,
                        FD[L1[di] - 1][L2[dj] - 1] + TD[di][dj]
                    )

    def compute_tree_distance(self, verbose=0):
        """Compute matrix `self._TD`."""

        self._TD[0][0] = 0

        for i in range(1, len(self._TD)):
            self._TD[i][0] = self._TD[i - 1][0] + self._del_cost
        for j in range(1, len(self._TD[0])):
            self._TD[0][j] = self._TD[0][j - 1] + self._ins_cost
        for kr1 in self._KR1:
            for kr2 in self._KR2:
                self._forest_dist(kr1, kr2, self._L1, self._L2, self._TD, verbose=verbose)
