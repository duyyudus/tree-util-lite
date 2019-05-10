import sys
from pathlib2 import Path

# Append parent directory of `tree_util_lite` package
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tree_util_lite.common.util import *
from tree_util_lite.core import tree, diff_engine


def build_tree_example():
    # From paths
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
    t = tree.Tree('test_tree', root_name='root', verbose=1)
    t.build_tree(paths)
    log_info('Render tree in hierarchy mode ( default ), without ID')
    t.render_tree()
    log_info('Render tree in directory mode, without ID')
    t.render_tree(directory_mode=1)
    log_info()

    # From dict
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
            'c1': {
                'c1a': {}
            },
            'c2': 'custom data'
        }
    }
    t = tree.Tree('test_tree', 'root', verbose=1)
    t.build_tree(hierarchy)
    log_info('Render tree in directory mode, with ID')
    t.render_tree(with_id=1, directory_mode=1)
    log_info('Render tree in hierarchy mode, node ID is irrelevant in hierarchy mode')
    t.render_tree(with_id=1)


def tree_diff_example():
    log_info('Building tree for tree diff...')
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
    t1 = tree.Tree('t1', 'root')
    t1.build_tree(p1)
    t1.render_tree()

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
    t2 = tree.Tree('t2', 'root')
    t2.build_tree(p2)
    t2.render_tree()

    differ = diff_engine.DiffEngine(t1, t2)
    log_info('Compute edit distance, show distance matrix and edit sequence in console')
    differ.compute_edit_sequence(show_matrix=1, show_edit=1)

    log_info('Process edit sequence and show diff data in console ( verbose=1 )')
    differ.postprocess_edit_sequence(verbose=1)

    differ.interpret_diff()

    # Another one
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

    diff = diff_engine.DiffEngine(t1, t2)
    log_info('Compute edit distance, show edit sequence in console')
    diff.compute_edit_sequence(show_matrix=0, show_edit=1)

    log_info('Process edit sequence and show diff data in console ( verbose=1 )')
    diff.postprocess_edit_sequence(verbose=1)

    diff.interpret_diff()


if __name__ == '__main__':
    build_tree_example()
    tree_diff_example()
