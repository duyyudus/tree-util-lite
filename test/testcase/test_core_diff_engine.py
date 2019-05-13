# Test trees
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
#                    root
#         ------------------------------
#         a        b1n     b2n     c_rel
#    -----------   ---   -------   ------
#    a1       a2   b1a   b2a b2b   c1  c2
#    ---      ---        ----
#    a1a      a2a        b2a1
# ----------
# a1a1  a1a3

from _setup_test import *
Tree = tree.Tree
Node = tree.Node


class TestCoreDiffEngine(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCoreDiffEngine, self).__init__(*args, **kwargs)

    def test_diff_engine(self):
        log_info()

        # Test 1
        p1 = [
            'a/a1/a1a/a1a1',
            'a/a1/a1a/a1a2',
            'a/a2/a2a',
            'b/b1/b1a',
            'b/b2/b2a',
            'b/b2/b2b',
            'c/c1',
            'c/c2',
        ]
        t1 = Tree('t1', 'root')
        t1.build_tree(p1)

        p2 = [
            'a/a1/a1a/a1a1',
            'a/a1/a1a/a1a3',
            'a/a2/a2a',
            'b1n/b1a',
            'b2n/b2a/b2a1',
            'b2n/b2b',
            'c_rel/c1',
            'c_rel/c2',
        ]
        t2 = Tree('t2', 'root')
        t2.build_tree(p2)

        differ = diff_engine.DiffEngine(t1, t2)
        differ.compute_edit_sequence(show_matrix=0, show_edit=1)
        differ.postprocess_edit_sequence()

        # Test 2
        p1 = [
            'medRes/asset.ma',
            'medRes/asset.rig.ma',
            'medRes/textures/tex_A_v1.tif',
            'medRes/textures/tex_B_v1.tif',
            'medRes/textures/tex_C_v1.tif',
            'proxyRes/asset.ma',
            'proxyRes/asset.rig.ma',
        ]
        t1 = tree.Tree('t1', root_name='last', verbose=1)
        t1.build_tree(p1)
        t1.render_tree()

        p2 = [
            'medRes/asset.ma',
            'medRes/asset.rig.ma',
            'medRes/textures/tex_A_v2.tif',
            'medRes/textures/tex_B_v1.tif',
            'medRes/textures/tex_C_v2.tif',
            'medRes/textures/tex_D_v1.tif',
            'medRes/old/asset.ma',
            'medRes/old/textures/tex_A_v1.tif',
            'medRes/old/textures/tex_C_v1.tif',
            'proxyRes/asset.ma',
            'proxyRes/asset.rig.ma',
        ]
        t2 = tree.Tree('t2', root_name='last', verbose=1)
        t2.build_tree(p2)
        t2.render_tree()

        differ = diff_engine.DiffEngine(t1, t2)
        differ.compute_edit_sequence(show_matrix=0, show_edit=1)
        differ.postprocess_edit_sequence(verbose=1)


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
