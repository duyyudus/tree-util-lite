import sys
from pathlib2 import Path

# Append parent directory of `tree_util_lite` package
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tree_util_lite.core import tree


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
    t.render_tree(without_id=1)
    print()

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
    t.render_tree(without_id=0)


if __name__ == '__main__':
    build_tree_example()
