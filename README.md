# tree-util-lite

A comprehensive generic ordered-tree data structure in Python, designed with easy to use API and developer friendly.

In fact, I made it for myself at first, after being tired of reinventing the wheel everytime I work on tree-like data.

It also come with Zhang Shasha tree-edit-distance algorithm, would be helpful for comparing trees.

### Supported properties/operations on a node of tree

By `tree_util_lite.core.tree.Node`

**Properties**

 * `verbose` (bool):
 * `label` (str):
 * `id` (str):
 * `path` (Path):
 * `parent` (Node):
 * `children` (list of Node):
 * `ancestor` (list of Node):
 * `descendant` (list of Node):
 * `sibling` (list of Node):
 * `child_count` (int):
 * `depth` (int):
 * `level` (int):
 * `height` (int):
 * `is_leaf` (bool):
 * `is_branch` (bool):
 * `is_root` (bool):
 * `is_isolated` (bool):
 * `data` (dict):

**Operations**

 * `set_verbose()`
 * `relabel()`
 * `set_parent()`
 * `add_children()`
 * `remove_children()`
 * `add_subpath()`
 * `contain_subpath()`
 * `traverse_preorder()`
 * `traverse_postorder()`
 * `traverse_levelorder()`
 * `render_subtree()`
 * `isolate()`
 * `insert()`
 * `delete()`
 * `cut_parent()`
 * `cut_children()`

### Supported properties/operations on tree

By `tree_util_lite.core.tree.Tree`

**Properties**

 * `tree_name` (str):
 * `root` (Node):

**Operations**

 * `build_tree()`
 * `ls()`
 * `search()`
 * `contain_path()`
 * `insert()`
 * `delete()`
 * `lowest_common_ancestor()`
 * `render_tree()`

## Example usages:

 * Representing hierarchical data
 * Detect changes in file/folder structures
 * Compare states in version control system
 * Differences between 3D scene hierarchies
 * So on...

Coming soon...