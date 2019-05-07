from tree_util_lite.common.util import *


class TreeDistance(object):
    """Base class for any tree-edit-distance algorithm.

    Implement most common properties and method of different tree distance algorithms.

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
        super(TreeDistance, self).__init__()
        self._r1 = r1
        self._r2 = r2
        self._del_cost = del_cost
        self._ins_cost = ins_cost
        self._rel_cost = rel_cost

        self._T1 = [None] + list(self._r1.nodes_by_postorder)
        self._T2 = [None] + list(self._r2.nodes_by_postorder)
        self._L1 = [self._T1.index(n.leftmost) if n else 0 for n in self._T1]
        self._L2 = [self._T2.index(n.leftmost) if n else 0 for n in self._T2]
        self._KR1 = [self._T1.index(n) for n in self._r1.keyroots]
        self._KR2 = [self._T2.index(n) for n in self._r2.keyroots]

        self._TD = [[0 for j in range(len(self._T2))] for i in range(len(self._T1))]

    @property
    def r1(self):
        """core.tree.Node: """
        return self._r1

    @property
    def r2(self):
        """core.tree.Node: """
        return self._r2

    @property
    def T1(self):
        """tuple of core.tree.Node: postorder sequence of nodes of tree rooted at `self._r1`."""
        return tuple(self._T1)

    @property
    def T2(self):
        """tuple of core.tree.Node: postorder sequence of nodes of tree rooted at `self._r2`."""
        return tuple(self._T2)

    @property
    def L1(self):
        """tuple of int: size = len(self.T1)

        L[i] is index in `self.T1` of leftmost leaf descendant of i'th node in `self.T1`

        Example, for below tree:

                      r1
                --------------
                a            b
            -----------   ----------
            a1       a2   b1      b2

               0     1     2    3     4     5    6    <---- index of items in T1
        T1 = ('a1', 'a2', 'a', 'b1', 'b2', 'b', 'r1')
        L1 = ( 0,    1,    0,   3,    4,    3,   0  )

        Explain:

            For i = 3, we have T1[3] is node 'b1',
            leftmost leaf descendant of 'b1' is itself as it has no children,
            index of 'b1' in T1 is 3,
            hence L[3] = 3

            For i = 6, we have T1[6] is node 'r1',
            leftmost leaf descendant of 'r1' is 'a1',
            index of 'a1' in T1 is 0,
            hence L[6] = 0

        """
        return tuple(self._L1)

    @property
    def L2(self):
        """tuple of int: size = len(self.T2)

        L[i] is index in `self.T2` of leftmost leaf descendant of i'th node in `self.T2`
        """
        return tuple(self._L2)

    @property
    def KR1(self):
        """tuple of int: sequence of indices in `self.T1` of keyroots of tree rooted at `self._r1`

        Example, for below tree:

                      r1
                --------------
                a            b
            -----------   ----------
            a1       a2   b1      b2
            ---           ---  --------
            a1a           b1a  b2a  b2b

                0      1     2     3    4      5     6      7      8     9    10    <---- index of items in T1
        T1  = ('a1a', 'a1', 'a2', 'a', 'b1a', 'b1', 'b2a', 'b2b', 'b2', 'b', 'r1')
        KR1 = (7, 2, 8, 9, 10)

        Explain:

            For i = 2, we have KR1[2] is 8 which is index in T1 of node 'b2'
            'b2' is a keyroot since it has left-sibling is 'b1'

            For i = 4, we have KR1[4] is 10 which is index in T1 of node 'r1'
            'r1' is a keyroot itself since it is root of the tree we are dealing with

        """
        return tuple(self._KR1)

    @property
    def KR2(self):
        """tuple of int: sequence of indices in `self.T2` of keyroots of tree rooted at `self._r2`"""
        return tuple(self._KR2)

    @property
    def TD(self):
        """tuple of tuple of int: 2-dimension array with size len(self.T1) x len(self.T2)

        Also known as "tree distance matrix"
        TD[i][j] is tree distance value of 2 subtree with root at `self.T1[i]` and `self.T2[j]`
        """
        return self._TD

    def compute_tree_distance(self):
        """This method must be implemented in all subclass of `TreeDistance`."""
        pass

    def compute_edit_sequence(self):
        """Compute edit sequence from `self._TD`."""
        edit_seq = []
        cursor = [len(self._TD) - 1, len(self._TD[0]) - 1]
        while cursor[0] >= 0 and cursor[1] >= 0:
            costs = [
                self._TD[cursor[0]][cursor[1] - 1] if cursor[1] > 0 else 99999,
                self._TD[cursor[0] - 1][cursor[1]] if cursor[0] > 0 else 99999,
                self._TD[cursor[0] - 1][cursor[1] - 1],
            ]
            min_cost_id = costs.index(min(costs))
            if min_cost_id == 0:
                # Insert operation
                edit_seq.insert(0, (None, self.T2[cursor[1] - 1]))
                cursor[1] -= 1
            elif min_cost_id == 1:
                # Delete operation
                edit_seq.insert(0, (self.T1[cursor[0] - 1], None))
                cursor[0] -= 1
            else:
                # Relabel operation
                edit_seq.insert(0, (self.T1[cursor[0] - 1], self.T2[cursor[1] - 1]))
                cursor[0] -= 1
                cursor[1] -= 1

        return edit_seq

    def show_matrix(self, matrix):
        print('')
        for row in matrix:
            s = ''.join([str(n) + ' ' * (4 - len(str(n))) for n in row])
            print(s)
        print('')

    def set_del_cost(self, cost):
        self._del_cost = cost

    def set_ins_cost(self, cost):
        self._ins_cost = cost

    def set_rel_cost(self, cost):
        self._rel_cost = cost
