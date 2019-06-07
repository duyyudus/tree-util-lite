import sys
from pathlib2 import Path

# Append parent directory of `tree_util_lite` package
sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from tree_util_lite.common.util import *
from tree_util_lite.core import tree, diff_engine
from tree_util_lite.diff_interpreter import binary_vcs_diff


def misc():
    log_info('Create path with data from inputs')
    print(tree.path_with_data('some/path', 'data'))


def build_tree_example():
    # From paths
    paths = [
        'a/a1/a1a/a1a1/_dx_0001',
        'a/a1/a1a/a1a2/_dx_0002',
        'a/a2/a2a/_dx_0003',
        'b/b1/b1a/_dx_0004',
        'b/b2/b2a/_dx_0005',
        'b/b2/b2b/_dx_0006',
        'c/c1/_dx_0007',
        'c/c2/_dx_0008',
    ]
    t = tree.Tree('test_tree', root_name='root', verbose=1)
    t.build_tree(paths)
    log_info('Render tree in hierarchy mode ( default ), without ID')
    t.render()
    log_info('Render tree in directory mode, without ID')
    t.render(directory_mode=1)
    log_info()
    log_info('All leaf nodes with data')
    log_info(t.ls_all_leaves())
    log_info()
    log_info('All leaf nodes relatively without data')
    log_info(t.ls_all_leaves(with_data=0, relative=1))
    log_info()
    log_info('Path with data of each node, absolute')
    for n in t.ls_all_leaves(with_data=1, as_path=0):
        print(n.path_with_data())
    log_info()
    log_info('Path with data of each node, relative')
    for n in t.ls_all_leaves(with_data=1, as_path=0):
        print(n.path_with_data(relative=1))

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
    t.render(with_id=1, directory_mode=1)
    log_info('Render tree in hierarchy mode, node ID is irrelevant in hierarchy mode')
    t.render(with_id=1)


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
    t1.render()

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
    t2.render()

    differ = diff_engine.DiffEngine(t1, t2)
    log_info('Compute edit distance, show distance matrix and edit sequence in console')
    differ.compute_edit_sequence(show_matrix=1, show_edit=1)

    log_info('Process edit sequence and show raw diff data in console ( verbose=1 )')
    differ.postprocess_edit_sequence(show_diff=1)

    # Another one, for asset versioning purpose
    p1 = [
        'medRes/asset.ma/_dx_h0001',
        'medRes/asset.rig.ma/_dx_h0002',
        'medRes/textures/tex_A_v1.tif/_dx_h0003',
        'medRes/textures/tex_B_v1.tif/_dx_h0004',
        'medRes/textures/tex_C_v1.tif/_dx_h0005',
        'proxyRes/asset.ma/_dx_h0006',
        'proxyRes/asset.rig.ma/_dx_h0007',
    ]
    t1 = tree.Tree('t1', root_name='last', verbose=1)
    t1.build_tree(p1)
    t1.render()

    p2 = [
        'medRes/asset.ma/_dx_h00012',
        'medRes/asset.rig.ma/_dx_h0002',
        'medRes/textures/tex_A_v2.tif/_dx_h00032',
        'medRes/textures/tex_B_v1.tif/_dx_h0004',
        'medRes/textures/tex_C_v2.tif/_dx_h00052',
        'medRes/textures/tex_D_v1.tif/_dx_h0008',
        'medRes/old/asset.ma/_dx_h0001',
        'medRes/old/backup_asset.rig.ma/_dx_h0002',
        'medRes/old/textures/tex_A_v1.tif/_dx_h0003',
        'medRes/old/textures/tex_C_v1.tif/_dx_h0005',
        'proxyRes/old_proxy_asset.ma/_dx_h0006',
    ]
    t2 = tree.Tree('t2', root_name='last', verbose=1)
    t2.build_tree(p2)
    t2.render()

    differ = diff_engine.DiffEngine(t1, t2)
    log_info('Compute edit distance, show edit sequence in console')
    differ.compute_edit_sequence(show_matrix=0, show_edit=1)

    log_info('Process edit sequence and show raw diff data in console ( verbose=1 )')
    differ.postprocess_edit_sequence(return_path=1, show_diff=1)

    log_info('Process edit sequence again but return real tree nodes instead of path')
    diff_data = differ.postprocess_edit_sequence(return_path=0, show_diff=0)

    log_info('Interpret raw diff data using binary file versioning convention and show in console')
    binary_vcs_diff.interpret(diff_data, return_path=1, show_diff=1)


if __name__ == '__main__':
    build_tree_example()
    tree_diff_example()
    misc()
