from _setup_test import *
Tree = tree.Tree
Node = tree.Node

# Test tree
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


class TestCoreTree(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCoreTree, self).__init__(*args, **kwargs)

    def test_tree_construction(self, verbose=1):
        log_info()
        t = Tree('test_tree', 'root', verbose=verbose)
        root = t.root
        a, b = root.add_children('a', 'b')

        a1, a1a, a1a1 = a.add_subpath('a1/a1a/a1a1')
        a1, a1a, a1a2 = a.add_subpath(Path('a1/a1a'), 'a1a2')

        a2, a2a = a.add_subpath(Node('a2'), 'a2a')

        self.assertTrue(root.contain_subpath('a/a1/a1a/a1a1'))
        self.assertTrue(root.contain_subpath('a/a1/a1a/a1a1'))
        self.assertTrue(root.contain_subpath('a/a2/a2a'))
        self.assertFalse(root.contain_subpath('a/a3/a3a'))

        b1 = Node('b1')
        b1.set_parent(b)
        b1a = Node('b1a')
        b1.add_children(b1a)
        b2 = Node('b2', parent=b)
        b2a, b2b = b2.add_children('b2a', 'b2b')

        self.assertTrue(b.contain_subpath('b1/b1a'))
        self.assertTrue(b.contain_subpath('b2/b2a'))
        self.assertTrue(b.contain_subpath('b2/b2b'))
        self.assertFalse(b.contain_subpath('b2/b2c'))

        c = root.add_children('c')[0]
        c1, c2 = c.add_children('c1', 'c2')

        self.assertTrue(root.contain_subpath('c/c1'))
        self.assertTrue(root.contain_subpath('c/c2'))
        self.assertFalse(root.contain_subpath('c/c2/c2a'))

        return t, root, a, b, c, a1, a1a2, a2a, b1a, c1

    def test_tree_traversal(self):
        log_info()
        t, root, a, b, c, a1, a1a2, a2a, b1a, c1 = self.test_tree_construction(verbose=0)

        root.render_subtree()
        log_info()
        a.render_subtree()
        log_info()

        # pre-order, stop at "b1"
        b.traverse_preorder(_print_visited_node)
        log_info()

        b_full = b.traverse_preorder(_return_visited_node)
        log_info(b_full)
        self.assertEqual(
            b_full,
            ['b', 'b1', 'b1a', 'b2', 'b2a', 'b2b']
        )
        b_stop = b.traverse_preorder(_return_visited_node_stop)
        log_info(b_stop)
        self.assertEqual(
            b_stop,
            ['b', 'b1']
        )
        log_info()

        # post-order, stop at "b1"
        root.traverse_postorder(_print_visited_node)
        log_info()

        root_full = root.traverse_postorder(_return_visited_node)
        log_info(root_full)
        self.assertEqual(
            root_full,
            [
                'a1a1',
                'a1a2',
                'a1a',
                'a1',
                'a2a',
                'a2',
                'a',
                'b1a',
                'b1',
                'b2a',
                'b2b',
                'b2',
                'b',
                'c1',
                'c2',
                'c',
                'root'
            ]
        )

        root_stop = root.traverse_postorder(_return_visited_node_stop)
        log_info(root_stop)
        self.assertEqual(
            root_stop,
            [
                'a1a1',
                'a1a2',
                'a1a',
                'a1',
                'a2a',
                'a2',
                'a',
                'b1a',
                'b1'
            ]
        )
        log_info()

        # level-order, stop at "b1"
        root.traverse_levelorder(_print_visited_node)
        log_info()

        root_full = root.traverse_levelorder(_return_visited_node)
        log_info(root_full)
        self.assertEqual(
            root_full,
            [
                'root',
                'a',
                'b',
                'c',
                'a1',
                'a2',
                'b1',
                'b2',
                'c1',
                'c2',
                'a1a',
                'a2a',
                'b1a',
                'b2a',
                'b2b',
                'a1a1',
                'a1a2'
            ]
        )

        root_stop = root.traverse_levelorder(_return_visited_node_stop)
        log_info(root_stop)
        self.assertEqual(
            root_stop,
            [
                'root',
                'a',
                'b',
                'c',
                'a1',
                'a2',
                'b1'
            ]
        )
        log_info()

    def test_node_property(self):
        log_info()
        t, root, a, b, c, a1, a1a2, a2a, b1a, c1 = self.test_tree_construction(verbose=0)

        self.assertEqual(b.depth, 1)
        self.assertEqual(a1.depth, 2)
        self.assertEqual(a1a2.depth, 4)
        self.assertEqual(a2a.depth, 3)
        self.assertEqual(b1a.depth, 3)
        self.assertEqual(c1.depth, 2)

        self.assertEqual(b.level, 1 + 1)
        self.assertEqual(a1.level, 2 + 1)
        self.assertEqual(a1a2.level, 4 + 1)
        self.assertEqual(a2a.level, 3 + 1)
        self.assertEqual(b1a.level, 3 + 1)
        self.assertEqual(c1.level, 2 + 1)

        self.assertEqual(b.height, 2)
        self.assertEqual(a1.height, 2)
        self.assertEqual(a1a2.height, 0)
        self.assertEqual(a2a.height, 0)
        self.assertEqual(b1a.height, 0)
        self.assertEqual(c1.height, 0)

        self.assertEqual(b.is_leaf, 0)
        self.assertEqual(a1.is_leaf, 0)
        self.assertEqual(a1a2.is_leaf, 1)
        self.assertEqual(a2a.is_leaf, 1)
        self.assertEqual(b1a.is_leaf, 1)
        self.assertEqual(c1.is_leaf, 1)

        self.assertEqual(b.is_branch, 1)
        self.assertEqual(a1.is_branch, 1)
        self.assertEqual(a1a2.is_branch, 0)
        self.assertEqual(a2a.is_branch, 0)
        self.assertEqual(b1a.is_branch, 0)
        self.assertEqual(c1.is_branch, 0)

        self.assertEqual(root.is_root, 1)
        self.assertEqual(a.is_root, 0)
        self.assertEqual(b.is_root, 0)
        self.assertEqual(a1.is_root, 0)
        self.assertEqual(a1a2.is_root, 0)
        self.assertEqual(a2a.is_root, 0)
        self.assertEqual(b1a.is_root, 0)
        self.assertEqual(c1.is_root, 0)

        self.assertEqual(b.node_path, Path('root/b'))
        self.assertEqual(a1.node_path, Path('root/a/a1'))
        self.assertEqual(a1a2.node_path, Path('root/a/a1/a1a/a1a2'))
        self.assertEqual(a2a.node_path, Path('root/a/a2/a2a'))
        self.assertEqual(b1a.node_path, Path('root/b/b1/b1a'))
        self.assertEqual(c1.node_path, Path('root/c/c1'))

        self.assertEqual(
            [n.label for n in b.ancestor],
            ['root']
        )
        self.assertEqual(
            [n.label for n in a1.ancestor],
            ['a', 'root']
        )
        self.assertEqual(
            [n.label for n in a1a2.ancestor],
            ['a1a', 'a1', 'a', 'root']
        )
        self.assertEqual(
            [n.label for n in a2a.ancestor],
            ['a2', 'a', 'root']
        )
        self.assertEqual(
            [n.label for n in b1a.ancestor],
            ['b1', 'b', 'root']
        )
        self.assertEqual(
            [n.label for n in c1.ancestor],
            ['c', 'root']
        )

        self.assertEqual(
            set([n.label for n in b.descendant]),
            set(['b1', 'b1a', 'b2', 'b2a', 'b2b'])
        )
        self.assertEqual(
            set([n.label for n in a1.descendant]),
            set(['a1a', 'a1a1', 'a1a2'])
        )
        self.assertEqual(
            set([n.label for n in a1a2.descendant]),
            set([])
        )
        self.assertEqual(
            set([n.label for n in a2a.descendant]),
            set([])
        )
        self.assertEqual(
            set([n.label for n in b1a.descendant]),
            set([])
        )
        self.assertEqual(
            set([n.label for n in c1.descendant]),
            set([])
        )

        self.assertEqual(
            [n.label for n in b.sibling],
            ['a', 'c']
        )
        self.assertEqual(
            [n.label for n in a1.sibling],
            ['a2']
        )

    def test_node_operation_error(self):
        log_info()
        t, root, a, b, c, a1, a1a2, a2a, b1a, c1 = self.test_tree_construction(verbose=0)

        # Test error scenarios when add children and set parent
        try:
            a.add_children('a2')
        except Exception as e:
            self.assertTrue(isinstance(e, tree.LabelClashing))
        try:
            Node('a1a').set_parent(a1)
        except Exception as e:
            self.assertTrue(isinstance(e, tree.LabelClashing))
        try:
            b.relabel('b')
        except Exception as e:
            self.assertTrue(isinstance(e, tree.LabelClashing))

        try:
            a1.set_parent(a1a2)
        except Exception as e:
            self.assertTrue(isinstance(e, tree.SetDescendantAsParent))
        try:
            c.set_parent(c1)
        except Exception as e:
            self.assertTrue(isinstance(e, tree.SetDescendantAsParent))

        try:
            b1a.add_children(b)
        except Exception as e:
            self.assertTrue(isinstance(e, tree.AddAncestorAsChild))
        try:
            a1.add_children(root)
        except Exception as e:
            self.assertTrue(isinstance(e, tree.AddAncestorAsChild))

        try:
            a2a.add_children(a2a)
        except Exception as e:
            self.assertTrue(isinstance(e, tree.SameNode))
        try:
            b.set_parent(b)
        except Exception as e:
            self.assertTrue(isinstance(e, tree.SameNode))

    def test_node_operation(self):
        log_info()
        t, root, a, b, c, a1, a1a2, a2a, b1a, c1 = self.test_tree_construction(verbose=0)
        b1, b2 = b.children

        # Test relabel
        b.relabel('b_relabeled')
        self.assertEqual(
            [n.label for n in root.children],
            ['a', 'b_relabeled', 'c']
        )
        b.relabel('b')

        # Test insert node
        c_inserted = c.insert('c_inserted')
        self.assertEqual([n.label for n in root.children], ['a', 'b', 'c_inserted'])
        self.assertEqual([n.label for n in c_inserted.children], ['c'])
        self.assertEqual(c.parent, c_inserted)

        # Test isolate node
        b.isolate()
        self.assertEqual(b.parent, None)
        self.assertEqual(b.children, [])
        self.assertEqual([n.label for n in root.children], ['a', 'c_inserted'])
        self.assertEqual(b1.parent, None)
        self.assertEqual(b2.parent, None)

        # Test remove children
        b2.remove_children('b2a')
        self.assertEqual([n.label for n in b2.children], ['b2b'])
        c.remove_children(c1, 'c2')
        self.assertEqual([n.label for n in c.children], [])

        # Test delete node
        a1a = a1.children[0]
        a1a.delete()
        self.assertEqual([n.label for n in a1.children], ['a1a1', 'a1a2'])
        self.assertEqual(a1a2.parent, a1)

        # Test cut node
        a.cut()
        self.assertEqual([n.label for n in root.children], ['c_inserted'])
        root.render_subtree()

    def test_tree_operation(self):
        log_info()
        t, root, a, b, c, a1, a1a2, a2a, b1a, c1 = self.test_tree_construction(verbose=0)

        self.assertEqual(root, root)
        new_root = Node('new_root')
        new_root.add_children(root)
        self.assertEqual(t.root, new_root)


def _print_visited_node(node):
    print(node.label)
    return 0, 0


def _return_visited_node(node):
    return node.label, 0


def _return_visited_node_stop(node):
    return node.label, 1 if node.label == 'b1' else 0


@log_test(__file__)
def run():
    switch_log(1)
    testcase_classes = [
        TestCoreTree
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
