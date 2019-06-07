# tree-util-lite

A comprehensive generic ordered-tree data structure in Python, designed with easy to use API and developer friendly.

In fact, I made it for myself at first, after being tired of reinventing the wheel everytime I work on tree-like data.

It also come with 2 tree distance algorithms

* Simple pre-order descendant alignment ( default )
* Zhang Shasha tree-edit-distance ( without postprocess implementation )

And a built-in raw diff interpreter dedicated for binary-file version control system, support following diff types

* added
* deleted
* renamed
* unchanged
* modified
* moved
* copied

They would be helpful for comparing trees.

## Supported properties/operations on a node of tree

By `tree_util_lite.core.tree.Node`

### **Properties**

* `verbose` (bool):
* `label` (str):
* `id` (str):
* `data` (any):
* `tmp_data` (any):
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
* `set_tmp_data()`
* `set_parent()`
* `add_children()`
* `remove_children()`
* `add_subpath()`
* `contain_subpath()`
* `traverse_preorder()`
* `traverse_postorder()`
* `traverse_levelorder()`
* `render()`
* `isolate()`
* `insert()`
* `delete()`
* `cut_parent()`
* `cut_children()`
* `lowest_common_ancestor()`
* `ls_all_leaves()`

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
* `ls_all_leaves()`
* `render()`

## Popular usages

* Representing hierarchical data
* Detect changes in file/folder structures
* Compare states in version control system
* Differences between 3D scene hierarchies
* So on...

## Usage examples

You can find example in `docs/usage_example.py`

### **1. First, we need to build some tree, there are two ways**

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

### **2. Basic tree diff**

There are 4 steps in tree diff computation

1. Compute tree distance using one of algorithms in `tree_distance`
2. Compute edit sequence from tree distance matrix
3. Postprocess edit sequence to raw diff data `DiffData`
4. Interpret raw diff data using one of interpreters in `diff_interpreter`

    * There is one built-in interpreter `binary_vcs_diff`, used for binary file versioning system

In this part, we will go through first 3 steps.

For 2 trees like below

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

Compute edit distance between 2 trees ( ***edit distance*** is the official term for difference between trees )

***distance matrix*** will also be computed here then showed with backtrack path and edit sequence in console

```python
differ = diff_engine.DiffEngine(t1, t2)
differ.compute_edit_sequence(show_matrix=1, show_edit=1)
```

```text
Distance matrix:

             root  a     a1    a1a   a1a1  a1a3  a2    a2a   b1n   b1a   b2n   b2a   b2a1  b2b   c_rel c1    c2
       0     1     2     3     4     5     6     7     8     9     10    11    12    13    14    15    16    17
 root  1    [0]    1     2     3     4     5     6     7     8     9     10    11    12    13    14    15    16
 a     2     1    [0]    1     2     3     4     5     6     7     8     9     10    11    12    13    14    15
 a1    3     2     1    [0]    1     2     3     4     5     6     7     8     9     10    11    12    13    14
 a1a   4     3     2     1    [0]    1     2     3     4     5     6     7     8     9     10    11    12    13
 a1a1  5     4     3     2     1    [0]    1     2     3     4     5     6     7     8     9     10    11    12
 a1a2  6     5     4     3     2     1    [1]    2     3     4     5     6     7     8     9     10    11    12
 a2    7     6     5     4     3     2     2    [1]    2     3     4     5     6     7     8     9     10    11
 a2a   8     7     6     5     4     3     3     2    [1]    2     3     4     5     6     7     8     9     10
 b     9     8     7     6     5     4     4     3     2    [2]    3     4     5     6     7     8     9     10
 b1    10    9     8     7     6     5     5     4     3    [3]    3     4     5     6     7     8     9     10
 b1a   11    10    9     8     7     6     6     5     4     4    [3]    4     5     6     7     8     9     10
 b2    12    11    10    9     8     7     7     6     5     5     4    [4]    5     6     7     8     9     10
 b2a   13    12    11    10    9     8     8     7     6     6     5     5    [4]   [5]    6     7     8     9
 b2b   14    13    12    11    10    9     9     8     7     7     6     6     5     5    [5]    6     7     8
 c     15    14    13    12    11    10    10    9     8     8     7     7     6     6     6    [6]    7     8
 c1    16    15    14    13    12    11    11    10    9     9     8     8     7     7     7     7    [6]    7
 c2    17    16    15    14    13    12    12    11    10    10    9     9     8     8     8     8     7    [6]

Edit sequence:

  root               -----------> root
  root/a             -----------> root/a
  root/a/a1          -----------> root/a/a1
  root/a/a1/a1a      -----------> root/a/a1/a1a
  root/a/a1/a1a/a1a1 -----------> root/a/a1/a1a/a1a1
  root/a/a1/a1a/a1a2 --relabel--> root/a/a1/a1a/a1a3
  root/a/a2          -----------> root/a/a2
  root/a/a2/a2a      -----------> root/a/a2/a2a
  root/b             --relabel--> root/b1n
  root/b/b1          --delete---> __
  root/b/b1/b1a      -----------> root/b1n/b1a
  root/b/b2          --relabel--> root/b2n
  root/b/b2/b2a      -----------> root/b2n/b2a
  __                 --insert---> root/b2n/b2a/b2a1
  root/b/b2/b2b      -----------> root/b2n/b2b
  root/c             --relabel--> root/c_rel
  root/c/c1          -----------> root/c_rel/c1
  root/c/c2          -----------> root/c_rel/c2
```

Process edit sequence and show ***raw diff data*** in console ( verbose=1 )

```python
differ.postprocess_edit_sequence(verbose=1)
```

```text
{'delete': ['root/b/b1',
            'root/b/b1/b1a',
            'root/b/b2',
            'root/b/b2/b2a',
            'root/b/b2/b2b',
            'root/c/c1',
            'root/c/c2'],
 'insert': ['root/b1n/b1a',
            'root/b2n',
            'root/b2n/b2a',
            'root/b2n/b2a/b2a1',
            'root/b2n/b2b',
            'root/c_rel/c1',
            'root/c_rel/c2'],
 'match': {'root': ('root', 'root'),
           'root/a': ('root/a', 'root/a'),
           'root/a/a1': ('root/a/a1', 'root/a/a1'),
           'root/a/a1/a1a': ('root/a/a1/a1a', 'root/a/a1/a1a'),
           'root/a/a1/a1a/a1a1': ('root/a/a1/a1a/a1a1', 'root/a/a1/a1a/a1a1'),
           'root/a/a2': ('root/a/a2', 'root/a/a2'),
           'root/a/a2/a2a': ('root/a/a2/a2a', 'root/a/a2/a2a')},
 'relabel': {'root/a/a1/a1a/a1a3': ('root/a/a1/a1a/a1a3', 'root/a/a1/a1a/a1a2'),
             'root/b1n': ('root/b1n', 'root/b'),
             'root/c_rel': ('root/c_rel', 'root/c')}}
```

***raw diff data*** always contain 4 keys

* delete
* insert
* match
* relabel

### **3. Advanced tree comparison**

Now we will dig deeper into ***interpret diff*** step

For 2 trees represent 2 folders of binary files

```python
from tree_util_lite.core import tree, diff_engine
from tree_util_lite.diff_interpreter import binary_vcs_diff

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
t1.render_tree()

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
t2.render_tree()
```

Here we can see the rightmost part of each path which start with `_dx_`, it means this part is not a node itself but it is `data` of the prior node.

In this case, it is treated as hash digest for the corresponding file. This data is not a part of the tree distance computation, we use it only to interpret ***raw diff data***.

Now, let's compute ***raw diff data***

```python
differ = diff_engine.DiffEngine(t1, t2)
differ.compute_edit_sequence(show_matrix=0, show_edit=1)
differ.postprocess_edit_sequence(return_path=1, verbose=1)
```

```text
Edit sequence:

  last                              -----------> last
  last/medRes                       -----------> last/medRes
  last/medRes/asset.ma              -----------> last/medRes/asset.ma
  last/medRes/asset.rig.ma          -----------> last/medRes/asset.rig.ma
  last/medRes/textures              -----------> last/medRes/textures
  last/medRes/textures/tex_A_v1.tif --relabel--> last/medRes/textures/tex_A_v2.tif
  last/medRes/textures/tex_B_v1.tif -----------> last/medRes/textures/tex_B_v1.tif
  last/medRes/textures/tex_C_v1.tif --relabel--> last/medRes/textures/tex_C_v2.tif
  last/proxyRes                     --relabel--> last/medRes/textures/tex_D_v1.tif
  __                                --insert---> last/medRes/old
  last/proxyRes/asset.ma            -----------> last/medRes/old/asset.ma
  last/proxyRes/asset.rig.ma        --relabel--> last/medRes/old/backup_asset.rig.ma
  __                                --insert---> last/medRes/old/textures
  __                                --insert---> last/medRes/old/textures/tex_A_v1.tif
  __                                --insert---> last/medRes/old/textures/tex_C_v1.tif
  __                                --insert---> last/proxyRes
  __                                --insert---> last/proxyRes/old_proxy_asset.ma

[Tree-Util-Lite] :: Raw diff data below:
[Tree-Util-Lite] ::
{'delete': ['last/proxyRes',
            'last/proxyRes/asset.ma',
            'last/proxyRes/asset.rig.ma'],
 'insert': ['last/medRes/textures/tex_D_v1.tif',
            'last/medRes/old',
            'last/medRes/old/asset.ma',
            'last/medRes/old/backup_asset.rig.ma',
            'last/medRes/old/textures',
            'last/medRes/old/textures/tex_A_v1.tif',
            'last/medRes/old/textures/tex_C_v1.tif',
            'last/proxyRes',
            'last/proxyRes/old_proxy_asset.ma'],
 'match': {'last': ('last', 'last'),
           'last/medRes': ('last/medRes', 'last/medRes'),
           'last/medRes/asset.ma': ('last/medRes/asset.ma',
                                    'last/medRes/asset.ma'),
           'last/medRes/asset.rig.ma': ('last/medRes/asset.rig.ma',
                                        'last/medRes/asset.rig.ma'),
           'last/medRes/textures': ('last/medRes/textures',
                                    'last/medRes/textures'),
           'last/medRes/textures/tex_B_v1.tif': ('last/medRes/textures/tex_B_v1.tif',
                                                 'last/medRes/textures/tex_B_v1.tif')},
 'relabel': {'last/medRes/textures/tex_A_v2.tif': ('last/medRes/textures/tex_A_v1.tif',
                                                   'last/medRes/textures/tex_A_v2.tif'),
             'last/medRes/textures/tex_C_v2.tif': ('last/medRes/textures/tex_C_v1.tif',
                                                   'last/medRes/textures/tex_C_v2.tif')}}
```

To interpret diff data, we must re-compute it and return with real `Node` objects instead of path by setting `return_path=0`

```python
diff_data = differ.postprocess_edit_sequence(return_path=0, show_diff=0)
```

And interpret it using built-in `diff_interpreter.binary_vcs_diff`

```python
binary_vcs_diff.interpret(diff_data, return_path=1, show_diff=1)
```

```text
[Tree-Util-Lite] :: Diff data in binary file versioning convention:
[Tree-Util-Lite] ::
{'added': ['last/medRes/textures/tex_D_v1.tif',
           'last/medRes/old/asset.ma',
           'last/medRes/textures/tex_A_v2.tif',
           'last/medRes/textures/tex_C_v2.tif'],
 'copied': {'last/medRes/old/backup_asset.rig.ma': ('last/medRes/asset.rig.ma',
                                                    'last/medRes/old/backup_asset.rig.ma')},
 'deleted': ['last/proxyRes/asset.rig.ma'],
 'modified': ['last/medRes/asset.ma'],
 'moved': {'last/medRes/old/textures/tex_A_v1.tif': ('last/medRes/textures/tex_A_v1.tif',
                                                     'last/medRes/old/textures/tex_A_v1.tif'),
           'last/medRes/old/textures/tex_C_v1.tif': ('last/medRes/textures/tex_C_v1.tif',
                                                     'last/medRes/old/textures/tex_C_v1.tif')},
 'renamed': {'last/proxyRes/old_proxy_asset.ma': ('last/proxyRes/asset.ma',
                                                  'last/proxyRes/old_proxy_asset.ma')},
 'unchanged': ['last/medRes/asset.rig.ma', 'last/medRes/textures/tex_B_v1.tif']}
```

Now you can check the above diff to see if it make sense.