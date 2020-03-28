#!/usr/bin/env python3


class Node(object):

    def __init__(self, data):
        self._data = data
        self._children = []

    def getdata(self):
        return self._data

    def getchildren(self):
        return self._children

    def add(self, node):
        ##if full
        if len(self._children) == 4:
            return False
        else:
            self._children.append(node)

    def go(self, data):
        for child in self._children:
            if child.getdata() == data:
                return child
        return None


class tree:

    def __init__(self):
        self._head = Node('header')

    def linktohead(self, node):
        self._head.add(node)

    def insert(self, path, data):
        cur = self._head
        for step in path:
            if cur.go(step) is None:
                return False
            else:
                cur = cur.go(step)
        cur.add(Node(data))
        return True

    def search(self, path):
        cur = self._head
        for step in path:
            if cur.go(step) is None:
                return None
            else:
                cur = cur.go(step)
        return cur


'''
define node
'''
a = Node('A')
b = Node('B')
c = Node('C')
d = Node('D')
e = Node('E')
f = Node('F')
g = Node('G')
h = Node('H')
i = Node('I')
j = Node('J')
k = Node('K')
l = Node('L')
m = Node('M')
n = Node('N')
o = Node('O')

'''
adding node to build true
'''
a.add(b)
a.add(g)
a.add(h)

b.add(c)
b.add(e)

g.add(i)
g.add(j)
g.add(k)
g.add(l)

h.add(m)
h.add(n)
h.add(o)

c.add(d)
c.add(f)

i.add(Node(29))
j.add(Node(28))
k.add(Node(27))
l.add(Node(26))
m.add(Node(25))
n.add(Node(24))
o.add(Node(23))
f.add(Node(30))

tree = tree()
tree.linktohead(a)

# testcase
print('Node', tree.search("ABE").getdata())
print('Node', tree.search("ABC").getdata())
print('Node', tree.search("AHM").getdata())
tree.insert("ABCD", 1)
for i in d.getchildren():
    print('value after', d.getdata(), ' is ', i.getdata())
