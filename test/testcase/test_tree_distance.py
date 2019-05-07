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
ZhangShasha = zhang_shasha.ZhangShasha


class TestTreeDistance(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTreeDistance, self).__init__(*args, **kwargs)

    def test_tree_distance_base(self):
        log_info()

        # Build test tree
        p1 = [
            'a/a1/a1a',
            'a/a2',
            'b/b1/b1a',
            'b/b2/b2a',
            'b/b2/b2b',
        ]
        t1 = tree.Tree('t1', root_name='r1', verbose=1)
        t1.build_tree(p1)
        # t1.render_tree(without_id=1)
        log_info()

        p2 = [
            'a/a1_rel/a1a',
            'a/a2',
            'c/c1',
            'b/b1_rel/b1a/b1a1',
            'b/b1_rel/b1b',
            'b/b2/b2a',
        ]
        t2 = tree.Tree('t2', root_name='r2', verbose=1)
        t2.build_tree(p2)
        # t2.render_tree(without_id=1)

        treedist = TreeDistance(t1.root, t2.root)

        # Test T1, T2
        # log_info([n.label for n in treedist.T1])
        self.assertEqual(treedist.T1, t1.root.nodes_by_postorder)
        # log_info([n.label for n in treedist.T2])
        self.assertEqual(treedist.T2, t2.root.nodes_by_postorder)

        # Test L1, L2
        self.assertEqual(
            treedist.L1,
            (0, 0, 2, 0, 4, 4, 6, 7, 6, 4, 0)
        )
        self.assertEqual(
            treedist.L2,
            (0, 0, 2, 0, 4, 4, 6, 6, 8, 6, 10, 10, 6, 0)
        )

        # Test KR1, KR2
        self.assertEqual(
            treedist.KR1,
            (7, 2, 8, 9, 10)
        )
        self.assertEqual(
            treedist.KR2,
            (8, 2, 11, 5, 12, 13)
        )

    def test_zhang_shasha(self):
        log_info()

        # Test 1
        p1 = [
            'a/a1/a1a',
            'a/a2',
            'b/b1/b1a',
            'b/b2/b2a',
            'b/b2/b2b',
        ]
        t1 = tree.Tree('t1', root_name='r1', verbose=1)
        t1.build_tree(p1)

        p2 = [
            'a/a1_rel/a1a',
            'a/a2',
            'c/c1',
            'b/b1_rel/b1a/b1a1',
            'b/b1_rel/b1b',
            'b/b2/b2a',
        ]
        t2 = tree.Tree('t2', root_name='r2', verbose=1)
        t2.build_tree(p2)

        treedist = ZhangShasha(t1.root, t2.root)
        treedist.compute_tree_distance()
        treedist.show_matrix(treedist.TD)

        # Test 2
        p1 = [
            'a',
            'b',
            'c'
        ]
        t1 = tree.Tree('t1', root_name='r1', verbose=1)
        t1.build_tree(p1)

        p2 = [
            'b',
            'c',
        ]
        t2 = tree.Tree('t2', root_name='r2', verbose=1)
        t2.build_tree(p2)

        treedist = ZhangShasha(t1.root, t2.root)
        treedist.compute_tree_distance()
        treedist.show_matrix(treedist.TD)

        edit_seq = treedist.compute_edit_sequence()
        for p in edit_seq:
            print(p[0].label if p[0] else 'None', '   ', p[1].label if p[1] else 'None')


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
