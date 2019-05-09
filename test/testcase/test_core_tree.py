from _setup_test import *
Tree = tree.Tree
Node = tree.Node

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


class TestCoreTree(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCoreTree, self).__init__(*args, **kwargs)

    def _test_tree_basic_construction(self, verbose=1):
        log_info()
        t = Tree('test_tree', 'root', verbose=verbose)
        root = t.root
        a, b = root.add_children('a', 'b')

        a1, a1a, a1a1 = a.add_subpath('a1/a1a/a1a1')
        a1, a1a, a1a2 = a.add_subpath(Path('a1/a1a'), 'a1a2')

        a2, a2a = a.add_subpath('a2', 'a2a')

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

    def _test_tree_advanced_construction(self):
        log_info()

        # Build from list of paths
        paths = [
            'a/a1/a1a/a1a1',
            'a/a1/a1a/a1a2',
            'a/a2/a2a',
            'b/b1/b1a',
            'b/b2/b2a',
            'b/b2/b2b',
            'c/c1',
            'c/c2',
        ]
        t = Tree('test_tree', 'root', verbose=1)
        t.build_tree(paths)
        # t.render_tree()
        for p in paths:
            self.assertTrue(t.contain_path('root/' + p))

        log_info()

        # Build from dict
        hierarchy = {
            'a': {
                'a1': {
                    'a1a': {
                        'a1a1': {},
                        'a1a2': {}
                    }
                }
            },
            'b': {
                'b1': {
                    'b1a': {}
                }
            },
            'c': {
                'c1': {},
                'c2': 'custom data'
            }
        }
        t = Tree('test_tree', 'root', verbose=1)
        t.build_tree(hierarchy)
        # t.render_tree()
        for p in [
            'root/a/a1/a1a/a1a1',
            'root/a/a1/a1a/a1a2',
            'root/b/b1/b1a',
            'root/c/c1',
        ]:
            self.assertTrue(t.contain_path(p))

    def _test_tree_traversal(self):
        log_info()
        t, root, a, b, c, a1, a1a2, a2a, b1a, c1 = self.test_tree_basic_construction(verbose=0)

        # pre-order from "b", stop at "b1"
        b.traverse_preorder(_print_visited_node)
        log_info()

        b_full = b.traverse_preorder(_return_visited_node)
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

        # post-order from "root", stop at "b1"
        root.traverse_postorder(_print_visited_node)
        log_info()

        root_full = root.traverse_postorder(_return_visited_node)
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

        # level-order from "root", stop at "b1"
        root.traverse_levelorder(_print_visited_node)
        log_info()

        root_full = root.traverse_levelorder(_return_visited_node)
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

    def _test_node_property(self):
        log_info()
        t, root, a, b, c, a1, a1a2, a2a, b1a, c1 = self.test_tree_basic_construction(verbose=0)

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

        self.assertEqual(b.path, Path('root/b'))
        self.assertEqual(a1.path, Path('root/a/a1'))
        self.assertEqual(a1a2.path, Path('root/a/a1/a1a/a1a2'))
        self.assertEqual(a2a.path, Path('root/a/a2/a2a'))
        self.assertEqual(b1a.path, Path('root/b/b1/b1a'))
        self.assertEqual(c1.path, Path('root/c/c1'))

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

    def _test_node_operation_error(self):
        log_info()
        t, root, a, b, c, a1, a1a2, a2a, b1a, c1 = self.test_tree_basic_construction(verbose=0)

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

    def _test_node_operation(self):
        log_info()
        t, root, a, b, c, a1, a1a2, a2a, b1a, c1 = self.test_tree_basic_construction(verbose=0)
        b1, b2 = b.children

        # Test lowest common ancestor
        self.assertEqual(a1a2.lowest_common_ancestor(a2a), a)
        self.assertEqual(a2a.lowest_common_ancestor(a1a2), a)
        self.assertEqual(a2a.lowest_common_ancestor(b1a), root)
        b2a, b2b = b2.children
        c.set_parent(b2)
        self.assertEqual(c1.lowest_common_ancestor(b2a), b2)
        c.set_parent(root)

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
        self.assertEqual(b2.is_isolated, 0)
        self.assertEqual(b.is_isolated, 1)

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
        a1.isolate()
        self.assertEqual(a1a2.is_isolated, 1)
        self.assertEqual([n.label for n in a.children], ['a2'])

        # Test cut node
        a.cut_parent()
        self.assertEqual([n.label for n in root.children], ['c_inserted'])
        root.render_subtree()
        log_info()

        # Test insert below
        c.add_children(c1, 'c2')
        c_inserted_below = c.insert('c_inserted_below', below=1)
        root.render_subtree()
        self.assertEqual(
            set([n.label for n in c_inserted_below.children]),
            set(['c1', 'c2'])
        )
        self.assertEqual([n.label for n in c.children], ['c_inserted_below'])
        self.assertEqual(c_inserted_below.parent, c)

    def _test_node_operation_advanced(self):
        log_info()
        t, root, a, b, c, a1, a1a2, a2a, b1a, c1 = self.test_tree_basic_construction(verbose=0)
        b1, b2 = b.children

        self.assertEqual(b.is_keyroot, 1)
        self.assertEqual(c.is_keyroot, 1)
        self.assertEqual(a1a2.is_keyroot, 1)
        self.assertEqual(b.leftmost, b1a)
        self.assertEqual(root.leftmost.label, 'a1a1')
        self.assertEqual(c1.leftmost, c1)
        self.assertEqual(b2.leftmost.label, 'b2a')
        self.assertEqual(
            [n.label for n in root.keyroots],
            [
                'a1a2',
                'b2b',
                'a2',
                'b2',
                'c2',
                'b',
                'c',
                'root',
            ]
        )
        self.assertEqual(
            [n.label for n in b.keyroots],
            [
                'b2b',
                'b2',
                'b',
            ]
        )
        self.assertEqual(
            [n.label for n in c.keyroots],
            [
                'c2',
                'c',
            ]
        )

        self.assertEqual(
            [n.label for n in root.nodes_by_postorder],
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
        self.assertEqual(
            [n.label for n in b.nodes_by_postorder],
            [
                'b1a',
                'b1',
                'b2a',
                'b2b',
                'b2',
                'b',
            ]
        )

    def _test_tree_property(self):
        log_info()
        t, root, a, b, c, a1, a1a2, a2a, b1a, c1 = self.test_tree_basic_construction(verbose=0)

        self.assertEqual(t.node_count, 17)
        self.assertEqual(root, root)
        new_root = Node('new_root')
        new_root.add_children(root)
        self.assertEqual(t.root, new_root)

        # Enumerate all nodes by traversal types
        self.assertEqual(
            [n.label for n in t.nodes_by_preorder],
            [
                'new_root',
                'root',
                'a',
                'a1',
                'a1a',
                'a1a1',
                'a1a2',
                'a2',
                'a2a',
                'b',
                'b1',
                'b1a',
                'b2',
                'b2a',
                'b2b',
                'c',
                'c1',
                'c2',
            ]
        )
        self.assertEqual(
            [n.label for n in t.nodes_by_postorder],
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
                'root',
                'new_root',
            ]
        )
        self.assertEqual(
            [n.label for n in t.nodes_by_levelorder],
            [
                'new_root',
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

    def _test_tree_operation(self):
        log_info()
        t, root, a, b, c, a1, a1a2, a2a, b1a, c1 = self.test_tree_basic_construction(verbose=0)
        b1, b2 = b.children

        # Test lowest common ancestor
        self.assertEqual(t.lowest_common_ancestor(a1a2, a2a), a)
        self.assertEqual(t.lowest_common_ancestor(a2a, a1a2), a)
        self.assertEqual(t.lowest_common_ancestor(a2a, b1a), root)
        b2a, b2b = b2.children
        c.set_parent(b2)
        self.assertEqual(t.lowest_common_ancestor(c1, b2a), b2)
        c.set_parent(root)

        # Test ls
        self.assertEqual(
            t.ls(return_label=1),
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
                'a1a2',
            ]
        )
        self.assertEqual(
            t.ls(a, return_label=1),
            [
                'a1',
                'a2',
                'a1a',
                'a2a',
                'a1a1',
                'a1a2',
            ]
        )
        self.assertEqual(
            t.ls(pattern='*1a1', return_label=1),
            [
                'a1a1',
            ]
        )
        self.assertEqual(
            t.ls(b, pattern='b/b2/*', return_label=1),
            [
                'b2a',
                'b2b',
            ]
        )
        self.assertEqual(
            t.ls(pattern='root/c/c1', return_label=1),
            [
                'c1',
            ]
        )
        self.assertEqual(
            t.ls(ids=[a.id, b1a.id], return_label=1),
            [
                'a',
                'b1a',
            ]
        )

        # Test search
        self.assertEqual(
            t.search('', return_label=1),
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
                'a1a2',
            ]
        )
        self.assertEqual(
            t.search('a2', return_label=1),
            [
                'a2',
            ]
        )
        self.assertEqual(
            t.search('root/b/*/*', return_label=1),
            [
                'b1a',
                'b2a',
                'b2b',
            ]
        )
        self.assertEqual(
            t.search('*/a1/*/*', return_label=1),
            [
                'a1a1',
                'a1a2',
            ]
        )
        self.assertEqual(
            t.search('', ids=[a.id, b1a.id], return_label=1),
            [
                'a',
                'b1a',
            ]
        )

        # Test insert
        c_inserted = Node('c_inserted')
        t.insert(c_inserted, c)
        self.assertEqual([n.label for n in root.children], ['a', 'b', 'c_inserted'])
        self.assertEqual([n.label for n in c_inserted.children], ['c'])
        self.assertEqual(c.parent, c_inserted)

        # Test delete
        a1a = a1.children[0]
        t.delete(a1a)
        self.assertEqual([n.label for n in a1.children], ['a1a1', 'a1a2'])
        self.assertEqual(a1a2.parent, a1)

    def test_tree_render(self):
        log_info()

        r = Node('r')
        r.add_subpath('a/a1')
        r.add_subpath('a/a2')
        r.add_subpath('b')
        r.add_subpath('c')
        r.render_subtree()

        t, root, a, b, c, a1, a1a2, a2a, b1a, c1 = self._test_tree_basic_construction(verbose=0)

        log_info('Render "{}"'.format(t.tree_name))
        root.render_subtree()
        log_info()
        log_info('Render subtree "a"')
        a.render_subtree()
        log_info()

        log_info('Render "{}" after deleting "a1"'.format(t.tree_name))
        a1.delete()
        root.render_subtree()
        log_info()

        log_info('Render "{}" after reparenting "c" to "b1a"'.format(t.tree_name))
        c.set_parent(b1a)
        root.render_subtree()
        log_info()

        log_info('Render "{}" after relabeling and insert "b2" to "b1a"'.format(t.tree_name))
        b1, b2 = b.children
        b2.relabel('b2_relabeled')
        b1a.insert(b2)
        root.render_subtree()
        log_info()

        log_info('Render "{}" after cutting "b2_relabeled" from the tree'.format(t.tree_name))
        b2.cut_parent()
        root.render_subtree()
        log_info()

        log_info('Render "{}" after adding "b2_relabeled" as child to "a"'.format(t.tree_name))
        a.add_children(b2)
        root.render_subtree()
        log_info()


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
