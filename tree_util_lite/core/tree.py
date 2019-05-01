from tree_util_lite.common.util import *

_STOP_TRAVERSAL = 0xffffffffffff


class InvalidBehavior(Exception):
    """Invalid behavior on Node."""


class SameNode(Exception):
    """Name point to the same node."""


class InvalidNode(Exception):
    """Invalid Node."""


class LabelClashing(Exception):
    """Name clashing when add child Node."""

    def __init__(self, label):
        super(LabelClashing, self).__init__()
        log_error('There is already a child Node with name "{}"'.format(label))


class Node(object):
    """Represent a node in tree.

    Attributes:
        _label (str):
        _data (dict):
        _parent (core.tree.Node):
        _children (list of core.tree.Node): Not exists if Node is file

    Properties:
        label (str):
        node_path (Path):
        parent (core.tree.Node):
        children (list of core.tree.Node):
        ancestor (list of core.tree.Node):
        descendant (list of core.tree.Node):
        child_count (int):
        depth (int):
        level (int):
        height (int):
        is_leaf (bool):
        is_branch (bool):
        is_root (bool):
        data (dict):

    Methods:
        relabel
        set_parent
        add_children
        add_subpath
        contain_subpath
        traverse_preorder
        traverse_postorder
        traverse_levelorder
        render_tree
        insert
        delete
        cut

    """

    def __init__(self, label, parent=None, data=None, verbose=0):
        """
        Args:
            label (str):
            parent (core.tree.Node):
            data (dict): custom data

        """

        super(Node, self).__init__()
        self._label = label
        self._data = data
        self._parent = parent
        self._children = []
        self._verbose = verbose

        self.set_parent(parent)

    @property
    def label(self):
        """str: """
        return self._label

    @property
    def data(self):
        """dict: """
        return self._data

    @property
    def child_count(self):
        """int: also known as the degree of node."""
        return len(self._children)

    @property
    def node_path(self):
        """Path: """
        cur_parent = self._parent
        parts = [self._label]
        while cur_parent:
            parts.insert(0, cur_parent.label)
            cur_parent = cur_parent.parent
        return Path(*parts)

    @property
    def depth(self):
        """int: """
        depth = 0
        cur_parent = self._parent
        while cur_parent:
            depth += 1
            cur_parent = cur_parent._parent
        return depth

    @property
    def level(self):
        """int: """
        level = 1
        cur_parent = self._parent
        while cur_parent:
            level += 1
            cur_parent = cur_parent._parent
        return level

    @property
    def height(self):
        """int: """
        def depth(node):
            return node.depth, 0

        return self.traverse_levelorder(depth)[-1] - self.depth

    @property
    def is_leaf(self):
        return 0 if self.children else 1

    @property
    def is_branch(self):
        return 1 if self.children else 0

    @property
    def is_root(self):
        return 1 if not self._parent else 0

    @property
    def parent(self):
        """core.tree.Node: """
        return self._parent

    @property
    def children(self):
        """list of core.tree.Node: """
        return self._children

    @property
    def ancestor(self):
        ret = []
        cur_parent = self.parent
        while cur_parent:
            ret.append(cur_parent)
            cur_parent = cur_parent.parent
        return ret

    @property
    def descendant(self):
        return self.traverse_preorder()[1:]

    def _validate_node(self, node):
        if node == self:
            raise SameNode()
        elif node == None:
            return 0
        elif not isinstance(node, Node):
            raise InvalidNode()
        else:
            return 1

    def relabel(self, label):
        """Relabel node after checking for label clashing."""
        pass

    def set_parent(self, parent):
        """
        Args:
            parent (core.tree.Node):
        """

        if not self._validate_node(parent):
            return 0

        # Remove `self` as child from current parent of `self`
        if self._parent != parent and self._parent:
            cur_parent = self._parent
            if self in cur_parent.children:
                cur_parent.children.remove(self)

        self._parent = parent

        if self._verbose:
            log_info('"{}" set "{}" as parent'.format(
                self.node_path,
                parent.node_path
            ))

        if self not in parent.children:
            parent.add_children(self)
        return 1

    def add_children(self, *args):
        """
        Args:
            args (list): mixed list of [str, core.tree.Node]
        """

        ret = []
        children = [Node(a) for a in args if isinstance(a, str) and a]
        children.extend([a for a in args if isinstance(a, Node)])
        for child in children:
            if not self._validate_node(child):
                continue

            for n in self._children:
                if n.label == child.label:
                    continue
            self._children.append(child)

            if self._verbose:
                log_info('"{}" added "{}" as child'.format(
                    self.node_path,
                    child.node_path
                ))

            if child.parent != self:
                child.set_parent(self)
            ret.append(child)
        return ret

    def add_subpath(self, *args):
        """
        Args:
            args (list): mixed list of [str, Path, core.tree.Node]
        """

        def to_part(a):
            if isinstance(a, (str, PurePath)):
                return str(a)
            elif isinstance(a, Node):
                return a.label
            else:
                return ''

        ret = []
        subpath = Path('/'.join([to_part(a) for a in args]))
        cur_node = self
        for label in subpath.parts:
            exists = 0
            for c in cur_node.children:
                if label == c.label:
                    cur_node = c
                    ret.append(cur_node)
                    exists = 1
                    break
            if not exists:
                cur_node = Node(label, parent=cur_node)
                ret.append(cur_node)
        return ret

    def contain_subpath(self, subpath):
        """Check if `subpath` is under `self` node.

        Args:
            subpath (str or Path): path of sub tree to be appended under `self`
        """

        subpath = Path(subpath)
        cur_node = self
        for label in subpath.parts:
            found = 0
            for c in cur_node.children:
                if c.label == label:
                    cur_node = c
                    found = 1
                    break
            if not found:
                return 0
        return 1

    def traverse_preorder(self, func=None):
        """Depth-first search.

        Args:
            func: function with node visit logic
                Must return 2-tuple:
                    (
                        visited: arbitrary value,
                        bool: stop traversal flag
                    )
                Default:
                    lambda node: (node, 0)
        Returns:
            list: list of visited node, the last one is "the one" node stop the traversal
        """

        if self._verbose:
            log_info('Start pre-order traversal on "{}"..'.format(self.node_path))

        if not func:
            func = lambda node: (node, 0)

        def _preorder(node, func):
            discovered = []

            # Visit `node`
            visited, stop = func(node)
            discovered.append(visited)
            if stop:
                discovered.append(_STOP_TRAVERSAL)

            # Visit sub trees of `node`
            for n in node.children:

                # Stop traversal condition
                if discovered[-1] == _STOP_TRAVERSAL:
                    return discovered

                discovered.extend(_preorder(n, func))
            return discovered

        ret = _preorder(self, func)
        return ret if ret[-1] != _STOP_TRAVERSAL else ret[:-1]

    def traverse_postorder(self, func=None):
        """Depth-first search.

        Args:
            func: function with node visit logic
                Must return 2-tuple:
                    (
                        visited: arbitrary value,
                        bool: stop traversal flag
                    )
                Default:
                    lambda node: (node, 0)
        Returns:
            list: list of visited node, the last one is "the one" node stop the traversal
        """

        if self._verbose:
            log_info('Start post-order traversal on "{}"..'.format(self.node_path))

        if not func:
            func = lambda node: (node, 0)

        def _postorder(node, func):
            discovered = []

            # Visit sub trees of `node`
            for n in node.children:
                subret = _postorder(n, func)
                discovered.extend(subret)

                # Stop traversal condition
                if subret[-1] == _STOP_TRAVERSAL:
                    return discovered

            # Visit `node`
            visited, stop = func(node)
            discovered.append(visited)
            if stop:
                discovered.append(_STOP_TRAVERSAL)
            return discovered

        ret = _postorder(self, func)
        return ret if ret[-1] != _STOP_TRAVERSAL else ret[:-1]

    def traverse_levelorder(self, func=None):
        """Breadth-first search.

        Args:
            func: function with node visit logic
                Must return 2-tuple:
                    (
                        visited: arbitrary value,
                        bool: stop traversal flag
                    )
                Default:
                    lambda node: (node, 0)
        Returns:
            list: list of visited node, the last one is "the one" node stop the traversal
        """

        if self._verbose:
            log_info('Start level-order traversal on "{}"..'.format(self.node_path))

        if not func:
            func = lambda node: (node, 0)

        discovered = []
        queue = [self]
        while queue:
            node = queue.pop()

            # Visit `node`
            visited, stop = func(node)
            discovered.append(visited)

            # Stop traversal condition
            if stop:
                return discovered

            for n in node.children:
                queue.insert(0, n)

        return discovered

    def render_tree(self):
        def print_indent(node):
            print('|---' * node.depth + node.label)
            return 0, 0
        self.traverse_preorder(print_indent)

    def insert(self, node, below=0):
        """Insert a new node at position right above `self`, make it new parent of `self`.

        Args:
            node (str or core.tree.Node): node to be inserted
                A new node will be created if a label is provided
            below (bool): insert below `self` instead
                All children of `self` will be re-parented to new node

        Returns:
            core.tree.Node:
        """

        return None

    def delete(self):
        """Delete `self` from linked nodes chain ( tree ).
        `self.children` will be re-parented to `self.parent`
        """

        pass

    def cut(self):
        """Disconnect `self` from its parent."""

        pass


class Tree(object):
    """A generic ordered-tree of Node objects.

    Attributes:
        _tree_name (str):
        _root (core.tree.Node):

    Properties:
        tree_name (str):
        root (core.tree.Node):

    Methods:
        ls
        search
        insert
        delete
        lowest_common_ancestor

    """

    def __init__(self, tree_name, root_name, verbose=0):
        """
        Args:
            tree_name (str):
            root_name (str):
        """

        super(Tree, self).__init__()
        self._tree_name = tree_name
        self._root = Node(
            '{}_root'.format(tree_name) if not root_name else root_name,
            verbose=verbose
        )

    @property
    def tree_name(self):
        """str: """
        return self._tree_name

    @property
    def root(self):
        """core.tree.Node: auto update new root."""
        root = self._root if not self._root.parent else self._root.ancestor[-1]
        return root

    def ls(self, node, pattern):
        """List nodes in tree.

        Args:
            node (core.tree.Node): list descendant of this node
                None for list all nodes in tree
            pattern (str): regex pattern

        Returns:
            list of core.tree.Node:
        """

        return []

    def search(self, node_path):
        """Search for a node using its label or node path in tree.

        Args:
            node_path (str or Path): path to node from `self._root`
                If a label is provided, search for all nodes with that

        Returns:
            list of core.tree.Node:
        """

        return []

    def insert(self, node, target):
        """
        Args:
            node (str or core.tree.Node):
            targe (str or Path or core.tree.Node):
        Returns:
            core.tree.Node:
        """

        return None

    def delete(self, node):
        """
        Args:
            node (str or Path or core.tree.Node):
        """

        pass

    def lowest_common_ancestor(self, node1, node2):
        """
        Returns:
            core.tree.Node:
        """

        return None
