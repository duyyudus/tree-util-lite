import copy
from tree_util_lite.common.util import *


class TreeDistance(object):
    """Base class for any tree-edit-distance algorithm.

    Implement most common properties and method of different tree distance algorithms.

    Attributes:
        _r1 (core.tree.Node):
        _r2 (core.tree.Node):

        _T1 (list of core.tree.Node): postorder sequence of nodes of tree rooted at `self._r1`
            None is put at the first position to represent null node
        _T2 (list of core.tree.Node): postorder sequence of nodes of tree rooted at `self._r2`
            None is put at the first position to represent null node

        _L1 (tuple of int): size = len(self._T1)
            L[i] is index in `self.T1` of leftmost leaf descendant of i'th node in `self._T1`
            Example, for below tree:

                          r1
                    --------------
                    a            b
                -----------   ----------
                a1       a2   b1      b2

                   0      1     2     3    4     5     6    7     <---- index of items in _T1
            _T1 = (None, 'a1', 'a2', 'a', 'b1', 'b2', 'b', 'r1')
            _L1 = (0,     1,    2,    1,   4,    5,    4,   1  )

            Explain:

                For i = 4, we have _T1[4] is node 'b1',
                leftmost leaf descendant of 'b1' is itself as it has no children,
                index of 'b1' in _T1 is 4,
                hence _L1[4] = 4

                For i = 7, we have _T1[7] is node 'r1',
                leftmost leaf descendant of 'r1' is 'a1',
                index of 'a1' in _T1 is 1,
                hence _L1[7] = 1

        _L2 (tuple of int): analog as _L1

        _KR1 (tuple of int): sequence of indices in `self._T1` of keyroots of tree rooted at `self._r1`
            Example, for below tree:

                          r1
                    --------------
                    a            b
                -----------   ----------
                a1       a2   b1      b2
                ---           ---  --------
                a1a           b1a  b2a  b2b

                    0      1      2     3     4    5      6     7      8      9     10   11  <---- index of items in _T1
            _T1  = (None, 'a1a', 'a1', 'a2', 'a', 'b1a', 'b1', 'b2a', 'b2b', 'b2', 'b', 'r1')
            _KR1 = (8, 3, 9, 10, 11)

            Explain:

                For i = 2, we have _KR1[2] is 9 which is index in _T1 of node 'b2'
                'b2' is a keyroot since it has left-sibling is 'b1'

                For i = 4, we have _KR1[4] is 11 which is index in _T1 of node 'r1'
                'r1' is a keyroot itself since it is root of the tree we are dealing with

        _KR2 (tuple of int): analog to _KR1

        _TD (list of list of int): 2-dimension array with size len(self._T1) x len(self._T2)
            Also known as "tree distance matrix"
            _TD[i][j] is tree distance value of 2 subtree with root at `self._T1[i]` and `self._T2[j]`

        _del_cost (int):
        _ins_cost (int):
        _rel_cost (int):

    Properties:
        r1 (core.tree.Node):
        r2 (core.tree.Node):
        TD (tuple of tuple of int): immutable version of self._TD

    Methods:
        compute_tree_distance
        compute_edit_sequence
        show_matrix
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

        self._T1 = tuple([None] + list(self._r1.nodes_by_postorder))
        self._T2 = tuple([None] + list(self._r2.nodes_by_postorder))
        self._L1 = tuple([self._T1.index(n.leftmost) if n else 0 for n in self._T1])
        self._L2 = tuple([self._T2.index(n.leftmost) if n else 0 for n in self._T2])
        self._KR1 = tuple([self._T1.index(n) for n in self._r1.keyroots])
        self._KR2 = tuple([self._T2.index(n) for n in self._r2.keyroots])

        self._TD = [[None for j in range(len(self._T2))] for i in range(len(self._T1))]

    @property
    def r1(self):
        """core.tree.Node: """
        return self._r1

    @property
    def r2(self):
        """core.tree.Node: """
        return self._r2

    @property
    def TD(self):
        td = []
        for row in self._TD:
            td.append(tuple(row))
        return tuple(td)

    def compute_tree_distance(self):
        """This method must be implemented in all subclass of `TreeDistance`."""
        pass

    def compute_edit_sequence(self, show_matrix=0):
        """Compute edit sequence from `self._TD`.

        Returns:
            list of 2-tuple: each tuple is an edit pair, a mapping from node in `self._T1` to one in `self._T2`
                (core.tree.Node, None): delete edit operation
                (None, core.tree.Node): insert edit operation
                (core.tree.Node, core.tree.Node): relabel edit operation

                `None` mean null node, represent for insert or delete operation
        """

        if show_matrix:
            distance_matrix = copy.deepcopy(self._TD)

        edit_seq = []
        cursor = [len(self._TD) - 1, len(self._TD[0]) - 1]
        while (cursor[0] + cursor[1]) > 0:
            distance_matrix[cursor[0]][cursor[1]] = '[{}]'.format(distance_matrix[cursor[0]][cursor[1]])

            min_cost_id = None
            if cursor[0] > 0 and cursor[1] > 0:
                if self._T1[cursor[0]].label == self._T2[cursor[1]].label:
                    min_cost_id = 2

            if not min_cost_id:
                costs = [
                    self._TD[cursor[0]][cursor[1] - 1] if cursor[1] > 0 else 0xffffffffff,
                    self._TD[cursor[0] - 1][cursor[1]] if cursor[0] > 0 else 0xffffffffff,
                    self._TD[cursor[0] - 1][cursor[1] - 1] if cursor[0] > 0 and cursor[1] > 0 else 0xffffffffff,
                ]
                min_cost_id = costs.index(min(costs))
            if min_cost_id == 0:
                # Insert operation
                edit_seq.insert(0, (None, self._T2[cursor[1]]))
                cursor[1] -= 1
            elif min_cost_id == 1:
                # Delete operation
                edit_seq.insert(0, (self._T1[cursor[0]], None))
                cursor[0] -= 1
            else:
                # Relabel operation
                edit_seq.insert(0, (self._T1[cursor[0]], self._T2[cursor[1]]))
                cursor[0] -= 1
                cursor[1] -= 1

        if show_matrix:
            for i, row in enumerate(distance_matrix):
                row.insert(0, self._T1[i].label if self._T1[i] else '')
            t2_row = [''] + [n.label if n else '' for n in self._T2]
            distance_matrix.insert(0, t2_row)
            self.show_matrix(distance_matrix)

        return edit_seq

    def show_matrix(self, matrix, min_column_size=4, column_spacing=1):
        print('')
        column_size = max([len(str(n)) + column_spacing for n in matrix[0]] + [min_column_size + column_spacing])
        print('Distance matrix:')
        print('')
        for row in matrix:
            if row[0] == '' and row[1] == '':
                s = ''.join([' ' + str(n) + ' ' * (column_size - len(str(n)) - 1) for n in row])
            else:
                s = ''.join(
                    [(' ' if not str(n).startswith('[') else '') +
                     str(n) + ' ' * (column_size - len(str(n)) - (1 if not str(n).startswith('[') else 0)) for n in row]
                )
            print(s)
        print('')

    def set_del_cost(self, cost):
        self._del_cost = cost

    def set_ins_cost(self, cost):
        self._ins_cost = cost

    def set_rel_cost(self, cost):
        self._rel_cost = cost
