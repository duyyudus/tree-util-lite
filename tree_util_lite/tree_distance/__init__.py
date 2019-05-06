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
        T1 (list of core.tree.Node): all postorder nodes of tree rooted at `_r1`
        T2 (list of core.tree.Node): all postorder nodes of tree rooted at `_r2`

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
        self._T1 = self._r1.nodes_by_postorder
        self._T2 = self._r2.nodes_by_postorder

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
        """list of core.tree.Node: all postorder nodes of tree rooted at `self._r1`."""
        return self._T1

    @property
    def T2(self):
        """list of core.tree.Node: all postorder nodes of tree rooted at `self._r2`."""
        return self._T2

    def set_del_cost(self, cost):
        self._del_cost = cost

    def set_ins_cost(self, cost):
        self._ins_cost = cost

    def set_rel_cost(self, cost):
        self._rel_cost = cost
