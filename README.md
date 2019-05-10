# tree-util-lite

A comprehensive generic ordered-tree data structure in Python, designed with easy to use API and developer friendly.

In fact, I made it for myself at first, after being tired of reinventing the wheel everytime I work on tree-like data.

It also come with 2 tree distance algorithms

* Simple post-order descendant alignment
* Zhang Shasha tree-edit-distance

They would be helpful for comparing trees.

## Supported properties/operations on a node of tree

By `tree_util_lite.core.tree.Node`

### **Properties**

* `verbose` (bool):
* `label` (str):
* `id` (str):
* `data` (dict):
* `child_count` (int):
* `path` (Path):
* `nice_path` (str):
* `depth` (int):
* `level` (int):
* `height` (int):
* `is_leaf` (bool):
* `is_branch` (bool):
* `is_root` (bool):
* `is_isolated` (bool):
* `is_keyroot` (bool):
* `parent` (Node):
* `children` (list of Node):
* `ancestor` (list of Node):
* `descendant` (list of Node):
* `sibling` (list of Node):
* `nodes_by_preorder` (list of Node):
* `nodes_by_postorder` (list of Node):
* `nodes_by_levelorder` (list of Node):
* `keyroots` (list of Node):
* `leftmost` (Node):

### **Operations**

* `set_verbose()`
* `relabel()`
* `set_data()`
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

## Supported properties/operations on tree

By `tree_util_lite.core.tree.Tree`

### **Properties**

* `tree_name` (str):
* `root` (Node):
* `node_count` (int):
* `nodes_by_preorder` (list of Node):
* `nodes_by_postorder` (list of Node):
* `nodes_by_levelorder` (list of Node):

### **Operations**

* `build_tree()`
* `ls()`
* `search()`
* `contain_path()`
* `insert()`
* `delete()`
* `lowest_common_ancestor()`
* `render_tree()`

## Popular usages

* Representing hierarchical data
* Detect changes in file/folder structures
* Compare states in version control system
* Differences between 3D scene hierarchies
* So on...

## Usage examples

You can find example in `docs/usage_example.py`

### Build tree, there are two ways

#### **1. From a list of node paths**

```python
from tree_util_lite.core import tree

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

```

Call `render_tree()` to check the result in console, by default tree is rendered in hierarchy mode without node ID

```python
t.render_tree()
```

```text
                    root
         ---------------------------
         a            b            c
    ----------   ----------     ------
    a1      a2   b1      b2     c1  c2
    ---     ---  ---  --------
    a1a     a2a  b1a  b2a  b2b
----------
a1a1  a1a2
```

Directory mode

```python
t.render_tree(directory_mode=1)
```

```text
root 
|---a 
|---|---a1 
|---|---|---a1a 
|---|---|---|---a1a1 
|---|---|---|---a1a2 
|---|---a2 
|---|---|---a2a 
|---b 
|---|---b1 
|---|---|---b1a 
|---|---b2 
|---|---|---b2a 
|---|---|---b2b 
|---c 
|---|---c1 
|---|---c2 
```

#### **2. From a dictionary**

```python
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
```

Check the result with node ID, only directory mode can show ID

```python
t.render_tree(with_id=1, directory_mode=1)
```

```text
root (o92c0lyx)
|---a (8ocgfarw)
|---|---a1 (yjp5c0vg)
|---|---|---a1a (gmcrz7n9)
|---|---|---|---a1a1 (nzcdogmp)
|---|---|---|---a1a2 (wfcj207v)
|---b (79ue5kqs)
|---|---b1 (pt510rfe)
|---|---|---b1a (25k6rhdx)
|---c (trpf2nza)
|---|---c1 (txmz3q4b)
|---|---|---c1a (aidwjfo7)
|---|---c2 (9fyb0xwa)
```
