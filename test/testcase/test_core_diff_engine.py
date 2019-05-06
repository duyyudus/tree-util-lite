# Test tree, preorder
#
# root
# |---a
# |---|---a1
# |---|---|---a1a
# |---|---|---|---a1a1
# |---|---|---|---a1a2
# |---|---a2
# |---|---|---a2a
# |---b
# |---|---b1
# |---|---|---b1a
# |---|---b2
# |---|---|---b2a
# |---|---|---b2b
# |---c
# |---|---c1
# |---|---c2

# Visualized in levelorder
#
#                    root
#         ---------------------------
#         a            b            c
#    -----------   ----------     ------
#    a1       a2   b1      b2     c1  c2
#    ---      ---  ---  --------
#    a1a      a2a  b1a  b2a  b2b
# ----------
# a1a1  a1a2
#
# parent_offset = len(children)/2 - len(parent)/2

from _setup_test import *
Tree = tree.Tree
Node = tree.Node


class TestCoreDiffEngine(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCoreDiffEngine, self).__init__(*args, **kwargs)

    def test_diff_engine(self):
        log_info()
        t1 = Tree('t1', 'r1')
        t2 = Tree('t2', 'r2')

        diff = diff_engine.DiffEngine(t1, t2)
        diff.compute_edit_sequence()
        diff.postprocess_edit_sequence()
        diff.interpret_diff()


@log_test(__file__)
def run():
    switch_log(1)
    testcase_classes = [
        TestCoreDiffEngine
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
