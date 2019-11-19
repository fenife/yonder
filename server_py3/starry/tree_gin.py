#!/usr/bin/env python3


from log import logger


# ErrDuplicatePath     = errors.New("Duplicate Path")
# ErrEmptyWildcardName = errors.New("Wildcards must be named with a non-empty name")
# ErrCatchAllConflict  = errors.New("CatchAlls are only allowed at the end of the path")
# ErrChildConflict     = errors.New("Can't insert a wildcard route because this path has existing children")
# ErrWildCardConflict  = errors.New("Conflict with wildcard route")


class ErrDuplicatePath(Exception):
    pass


class ErrEmptyWildcardName(Exception):
    pass


class ErrCatchAllConflict(Exception):
    pass


class ErrChildConflict(Exception):
    pass


class ErrWildCardConflict(Exception):
    pass


class Node(object):
    def __init__(self, key=None, indices=[], children=[], value=None,
                 wildChild=False, isParm=False, isCatchAll=False):
        self.key = key
        self.indices = indices
        self.children = children
        self.value = value
        self.wildChild = wildChild
        self.isParm = isParm
        self.isCatchAll = isCatchAll

    @staticmethod
    def printChildren(node, prefix):
        print(f"{prefix}{node.key}[{len(node.children)}] {node.value}")
        l = len(node.key)
        while l > 0:
            prefix += ' '
            l = l - 1

        for child in node.children:
            node.printChildren(child, prefix)

    def addRoute(self, key, value):
        logger.debug(f'add route: {key}')
        # if len(self.key) == 0:
        if not self.key:
            return self.insertRoute(key, value)

        while True:
            while True:
                i = 0
                j = min(len(key), len(self.key))
                # find the longest prefix
                while i < j and key[i] == self.key[i]:
                    i += 1

                if i < len(self.key):
                    child = Node(
                        key=self.key[i:],
                        indices=self.indices,
                        children=self.children,
                        value=self.value,
                        wildChild=self.wildChild,
                    )
                    self.children = [child]
                    self.indices = [self.key[i]]
                    self.value = None
                    self.wildChild = False

                if i < len(key):
                    key = key[i:]

                    if self.wildChild:
                        self = self.children[0]

                        if len(key) > len(self.key) and self.key == key[:len(self.key)]:
                            if len(self.key) < len(key) and key[len(self.key)] != '/':
                                raise ErrWildCardConflict
                            else:
                                break
                        else:
                            raise ErrWildCardConflict

                    c = key[0]

                    if self.isParm and c == '/' and len(self.children) == 1:
                        n = self.children[0]
                        break

                    for i, index in enumerate(self.indices):
                        if c == index:
                            self = self.children[i]
                            break

                    if c != ':' and c != '*':
                        self.indices.append(c)
                        child = Node()
                        self.children.append(child)
                        self = child

                    return self.insertRoute(key, value)

                elif i == len(key):
                    if self.value is not None:
                        raise ErrDuplicatePath
                    self.value = value

                return None

    def insertRoute(self, key, value):
        offset = 0
        i, j = 0, len(key)
        while i < j:
            b = key[i]
            logger.debug(f'i: {i}, j: {j}, b: {b}, self.key: {self.key}')
            if b == ':' or b == '*':
                if len(self.children) > 0:
                    raise ErrChildConflict

                k = i + 1
                while k < j and key[k] != '/':
                    k += 1

                if (k-i) == 1:
                    raise ErrEmptyWildcardName

                if b == '*' and len(key) != k:
                    raise ErrCatchAllConflict

                child = Node()
                if b == ':':
                    child.isParm = True
                else:
                    child.isCatchAll = True

                if i > 0:
                    self.key = key[offset:i]
                    offset = i

                self.children = [child]
                self.wildChild = True
                self = child

            i += 1

        self.key = key[offset:]
        self.value = value


def getValue(n, key):
    assert isinstance(n, Node), 'node type error'

    logger.debug(f"key: {key}, n.key: {n.key}")

    value = None
    _vars = None
    tsr = None

    while True:
        while len(key) >= len(n.key) and key[:len(n.key)] == n.key:
            if len(key) == len(n.key):
                value = n.value
                if value is not None:
                    return value, _vars, tsr

                for i, index in enumerate(n.indices):
                    if index == '/':
                        tsr = n.children[i].key == '/' and n.children[i].value is not None
                        return value, _vars, tsr
                return value, _vars, tsr

            elif n.wildChild is True:
                key = key[len(n.key):]
                n = n.children[0]

                if n.isParm:
                    k = 0
                    l = len(key)
                    while k < l and key[k] != '/':
                        k += 1

                    if not _vars:
                        _vars = {
                            n.key[1:]: key[:k],
                        }
                    else:
                        _vars[n.key[1:]] = key[:k]

                    if k < l:
                        if len(n.children) > 0:
                            key = key[k:]
                            n = n.children[0]
                            continue
                        else:
                            tsr = l == k+1
                            return value, _vars, tsr

                    value = n.value
                    if value is not None:
                        return value, _vars, tsr
                    elif len(n.children) == 1:
                        n = n.children[0]
                        tsr = n.key == '/' and n.value is not None

                    return value, _vars, tsr

                else:
                    if not _vars:
                        _vars = {n.key[1:]: key}
                    else:
                        _vars[n.key[1:]] = key

                    value = n.value
                    return value, _vars, tsr

            key = key[len(n.key):]
            c = key[0]

            for i, index in enumerate(n.indices):
                if c == index:
                    n = n.children[i]
                    break

            tsr = key == '/' and n.value is not None
            return value, _vars, tsr

        tsr = (n.value is not None and len(key)+1 == len(n.key) and n.key[len(key)] == '/') or (key == '/')
        return value, _vars, tsr
