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

### **1. Build tree, there are two ways**

#### *From a list of node paths*

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

#### *From a dictionary*

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

### **2. Compare trees**

First, we build 2 trees

```python
from tree_util_lite.core import tree, diff_engine

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


                      root
         ------------------------------
         a       b1n      b2n     c_rel
    ----------   ---   --------  ------
    a1      a2   b1a   b2a  b2b  c1  c2
    ---     ---       ----
    a1a     a2a       b2a1
----------
a1a1  a1a3
```

Compute edit distance between 2 trees ( ***edit distance*** is official term for difference between trees )

It will show distance matrix with backtrack path and edit sequence in console

```python
differ = diff_engine.DiffEngine(t1, t2)
differ.compute_edit_sequence(show_matrix=1, show_edit=1)
```

```text
Distance matrix:

             a1a1  a1a3  a1a   a1    a2a   a2    a     b1a   b1n   b2a1  b2a   b2b   b2n   c1    c2    c_rel root
       0     1     2     3     4     5     6     7     8     9     10    11    12    13    14    15    16    17
 a1a1  1    [0]    1     2     3     4     5     6     7     8     9     10    11    12    13    14    15    16
 a1a2  2     1    [1]    2     3     4     5     6     7     8     9     10    11    12    13    14    15    16
 a1a   3     2     2    [1]    2     3     4     5     6     7     8     9     10    11    12    13    14    15
 a1    4     3     3     2    [1]    2     3     4     5     6     7     8     9     10    11    12    13    14
 a2a   5     4     4     3     2    [1]    2     3     4     5     6     7     8     9     10    11    12    13
 a2    6     5     5     4     3     2    [1]    2     3     4     5     6     7     8     9     10    11    12
 a     7     6     6     5     4     3     2    [1]    2     3     4     5     6     7     8     9     10    11
 b1a   8     7     7     6     5     4     3     2    [1]    2     3     4     5     6     7     8     9     10
 b1    9     8     8     7     6     5     4     3     2    [2]   [3]    4     5     6     7     8     9     10
 b2a   10    9     9     8     7     6     5     4     3     3     3    [3]    4     5     6     7     8     9
 b2b   11    10    10    9     8     7     6     5     4     4     4     4    [3]    4     5     6     7     8
 b2    12    11    11    10    9     8     7     6     5     5     5     5     4    [4]    5     6     7     8
 b     13    12    12    11    10    9     8     7     6     6     6     6     5    [5]    5     6     7     8
 c1    14    13    13    12    11    10    9     8     7     7     7     7     6     6    [5]    6     7     8
 c2    15    14    14    13    12    11    10    9     8     8     8     8     7     7     6    [5]    6     7
 c     16    15    15    14    13    12    11    10    9     9     9     9     8     8     7     6    [6]    7
 root  17    16    16    15    14    13    12    11    10    10    10    10    9     9     8     7     7    [6]

Edit sequence:

  a1a1 -----------> a1a1
  a1a2 --relabel--> a1a3
  a1a  -----------> a1a
  a1   -----------> a1
  a2a  -----------> a2a
  a2   -----------> a2
  a    -----------> a
  b1a  -----------> b1a
  b1   --relabel--> b1n
  __   --insert---> b2a1
  b2a  -----------> b2a
  b2b  -----------> b2b
  b2   --relabel--> b2n
  b    --delete---> __
  c1   -----------> c1
  c2   -----------> c2
  c    --relabel--> c_rel
  root -----------> root
```

Process edit sequence and show diff data in console ( verbose=1 )

```python
differ.postprocess_edit_sequence(verbose=1)
```

```text
{'delete': ['root/b'],
 'insert': ['root/b2n/b2a/b2a1'],
 'match': {'root': 'root',
           'root/a': 'root/a',
           'root/a/a1': 'root/a/a1',
           'root/a/a1/a1a': 'root/a/a1/a1a',
           'root/a/a1/a1a/a1a1': 'root/a/a1/a1a/a1a1',
           'root/a/a2': 'root/a/a2',
           'root/a/a2/a2a': 'root/a/a2/a2a',
           'root/b1n/b1a': 'root/b/b1/b1a',
           'root/b2n/b2a': 'root/b/b2/b2a',
           'root/b2n/b2b': 'root/b/b2/b2b',
           'root/c_rel/c1': 'root/c/c1',
           'root/c_rel/c2': 'root/c/c2'},
 'relabel': {'root/a/a1/a1a/a1a3': 'root/a/a1/a1a/a1a2',
             'root/b1n': 'root/b/b1',
             'root/b2n': 'root/b/b2',
             'root/c_rel': 'root/c'}}
```
