# Zhang Shasha tree edit distance algorithm

from tree_util_lite.common.util import *
from . import TreeDistance


class ZhangShasha(TreeDistance):
    """Zhang Shasha algo

    Inherit from `TreeDistance`

    Attributes:
        _r1 (core.tree.Node):
        _r2 (core.tree.Node):
        _T1 (list of core.tree.Node): all postorder nodes of tree rooted at `_r1`
        _T2 (list of core.tree.Node): all postorder nodes of tree rooted at `_r2`
        _del_cost (int):
        _ins_cost (int):
        _rel_cost (int):

    Properties:
        r1 (core.tree.Node):
        r2 (core.tree.Node):
        T1 (tuple of core.tree.Node): all postorder nodes of tree rooted at `_r1`
        T2 (tuple of core.tree.Node): all postorder nodes of tree rooted at `_r2`
        L1 (tuple of int): L[i] is index in `self.T1` of leftmost leaf descendant of i'th node in `self.T1`
        L2 (tuple of int): L[i] is index in `self.T2` of leftmost leaf descendant of i'th node in `self.T2`
        KR1 (tuple of int): sequence of indices in `self.T1` of keyroots of tree rooted at `self._r1`
        KR2 (tuple of int): sequence of indices in `self.T2` of keyroots of tree rooted at `self._r2`

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

    def _forest_dist(self, i, j, L1, L2, TD):
        log_info('Compute distance between subtree pair at keyroot: T1[{}] -> T2[{}]'.format(i, j))

        # Temporary forest distance matrix
        FD = [[None for j in range(len(self._T2))] for i in range(len(self._T1))]

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
                        FD[di - 1][dj - 1] + (self._rel_cost if self.T1[di].label != self.T2[dj].label else 0)
                    )
                    TD[di][dj] = FD[di][dj]
                    # print('----Updated subtree distance: T1[{}] -> T2[{}]'.format(di, dj))
                else:
                    FD[di][dj] = min(
                        FD[di - 1][dj] + self._del_cost,
                        FD[di][dj - 1] + self._ins_cost,
                        FD[L1[di] - 1][L2[dj] - 1] + TD[di][dj]
                    )

    def compute_tree_distance(self):
        """Compute matrix `self._TD`."""

        for i in range(1, len(self._TD)):
            self._TD[i][0] = self._TD[i - 1][0] + self._del_cost
        for j in range(1, len(self._TD[0])):
            self._TD[0][j] = self._TD[0][j - 1] + self._ins_cost
        for kr1 in self.KR1:
            for kr2 in self.KR2:
                self._forest_dist(kr1, kr2, self.L1, self.L2, self._TD)
