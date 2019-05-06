# Test trees
#
#             r1
#       --------------
#       a            b
#   -----------   ----------
#   a1       a2   b1      b2
#   ---           ---  --------
#   a1a           b1a  b2a  b2b
#
#               r2
#       --------------------
#       a        c         b
#   -----------  --  -------------
#   a1_rel   a2  c1  b1_rel     b2
#   ------           ---------  ---
#   a1a              b1a   b1b  b2a
#                    ----
#                    b1a1

from _setup_test import *
Tree = tree.Tree
Node = tree.Node
TreeDistance = tree_distance.TreeDistance


class TestTreeDistance(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTreeDistance, self).__init__(*args, **kwargs)

    def test_tree_distance_base(self):
        log_info()
        p1 = [
            'a/a1/a1a',
            'a/a2',
            'b/b1/b1a',
            'b/b2/b2a',
            'b/b2/b2b',
        ]
        t1 = tree.Tree('t1', root_name='r1', verbose=1)
        t1.build_tree(p1)
        t1.render_tree(without_id=1)
        log_info()

        p1 = [
            'a/a1_rel/a1a',
            'a/a2',
            'c/c1',
            'b/b1_rel/b1a/b1a1',
            'b/b1_rel/b1b',
            'b/b2/b2a',
        ]
        t2 = tree.Tree('t2', root_name='r2', verbose=1)
        t2.build_tree(p1)
        t2.render_tree(without_id=1)

        treedist = TreeDistance(t1.root, t2.root)

        log_info([n.label for n in treedist.T1])
        self.assertEqual(treedist.T1, t1.root.nodes_by_postorder)
        log_info([n.label for n in treedist.T2])
        self.assertEqual(treedist.T2, t2.root.nodes_by_postorder)


@log_test(__file__)
def run():
    switch_log(1)
    testcase_classes = [
        TestTreeDistance
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
