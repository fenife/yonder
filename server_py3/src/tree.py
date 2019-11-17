#!/usr/bin/env python3


class Node(object):
    def __init__(self, key=None, handler=None, isWildcard=None):
        self.key = key
        self.handler = handler
        self.children = []
        self.isWildcard = isWildcard     # 通配符节点

    def __repr__(self):
        return f"<{self.key}{'' if not self.handler else ' - ' + self.handler.__name__}>"


_root = Node(key='/')


def printChildren(node, depth):
    assert isinstance(node, Node), 'node must be a Node object'

    if not node.children:
        return

    print(' ' * depth, node.children)

    for child in node.children:
        printChildren(child, depth+1)


def insertRemained(node, keys):
    if not keys:
        return

    for key in keys:
        new = Node(key=key)
        node.children.append(new)
        node = new

    return node


def addNode(node, keys):
    assert isinstance(node, Node), 'node must be a Node object'
    if not keys:
        return

    # 没有子节点，插入剩余全部的key
    if not node.children:
        last = insertRemained(node, keys)

    # 取第一个key，对比node的子节点，
    # 如果对的上，取下一级的节点继续对比
    # 如果对不上，插入剩余的keys
    key = keys[0]
    for child in node.children:
        if child.key == key:
            addNode(child, keys[1:])
            return

    last = insertRemained(node, keys)


def addRoute(path, handler):
    pathKeys = path.split('/')
    print(path)
    print(pathKeys)

    if path.endswith('/'):
        pathKeys.append('/')

    print(pathKeys)
    addNode(_root, pathKeys)


def _test():
    def hello():
        print("hello world")

    path = 'a/b/c/:x'
    addRoute(path, hello)

    path = 'a/b/c/d/*y'
    addRoute(path, hello)

    print()
    printChildren(_root, 0)


if __name__ == "__main__":
    _test()
