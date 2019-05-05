# Zhang Shasha tree edit distance algorithm

from tree_util_lite.common.util import *
from . import TreeDistance


class ZhangShasha(TreeDistance):
    """Zhang Shasha algo"""

    def __init__(self, t1, t2):
        """
        Args:
            t1 (core.tree.Node): root of tree 1
            t2 (core.tree.Node): root of tree 2
        """
        super(ZhangShasha, self).__init__(t1, t2)

    def compute_edit_sequence(self):
        log_info('Computed edit sequence from "{}"-rooted tree to "{}"-rooted tree'.format(
            self.t1.label, self.t2.label
        ))
