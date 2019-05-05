class TreeDistance(object):
    """TreeDistance base class.

    Attributes:
        _t1 (core.tree.Node):
        _t2 (core.tree.Node):
        _del_cost (int):
        _ins_cost (int):
        _rel_cost (int):

    Properties:
        t1 (core.tree.Node):
        t2 (core.tree.Node):

    Methods:
        set_del_cost
        set_ins_cost
        set_rel_cost

    """

    def __init__(self, t1, t2, del_cost=1, ins_cost=1, rel_cost=1):
        """
        Args:
            t1 (core.tree.Node): root of tree 1
            t2 (core.tree.Node): root of tree 2
            del_cost (int): cost of delete edit operation
            ins_cost (int): cost of insert edit operation
            rel_cost (int): cost of relabel edit operation
        """
        super(TreeDistance, self).__init__()
        self._t1 = t1
        self._t2 = t2
        self._del_cost = del_cost
        self._ins_cost = ins_cost
        self._rel_cost = rel_cost

    @property
    def t1(self):
        """core.tree.Node: """
        return self._t1

    @property
    def t2(self):
        """core.tree.Node: """
        return self._t2

    def set_del_cost(self, cost):
        self._del_cost = cost

    def set_ins_cost(self, cost):
        self._ins_cost = cost

    def set_rel_cost(self, cost):
        self._rel_cost = cost
