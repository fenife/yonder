#!/usr/bin/env python3


class Node(object):
    def __init__(self, key=None, handler=None):
        self.key = key
        self.path = None
        self.path = ''

        self.handler = handler
        # self._parent = None
        self.children: [Node] = []
        # 是否是通配符节点
        # `:`匹配路径中的单个key，`*`匹配url中剩余的所有内容
        self.wildcard = True if self.key and self.key[0] in (':', '*') else False
        # 通配符所在的子节点
        self.wildcard_child = None

    def get_path(self):
        return self.path

    def get_handler(self):
        return self.handler

    def __repr__(self):
        return f"<{self.key}{'' if not self.handler else ' - ' + self.handler.__name__}>"

    def add_child(self, child):
        """添加子节点"""
        # 拼接到该节点为止的完整path
        if self.key.endswith('/') or child.key.startswith('/'):
            child_path = self.path + child.key
        else:
            child_path = self.path + '/' + child.key

        # 同一个节点的子节点下，只能有一种通配符, `:`或者`*`
        if self.wildcard_child and child.wildcard:
            s = f"wildcard has been existed in children: " \
                f"{self.wildcard_child.get_path()}, this path: {child_path}"
            raise Exception(s)

        # child.parent = self
        child.path = child_path
        self.children.append(child)

        if child.wildcard:
            self.wildcard_child = child

    def find_child(self, key):
        """查找具有相同key的子节点"""
        for child in self.children:
            if child.key == key:
                return child

        return None


class Tree(object):
    def __init__(self):
        self._root = Node(key='')
        self._map = {}

    @staticmethod
    def path_to_keys(path):
        """
        把path转换为keys

        1. 首字符必须为'/'，作为第一个key
        2. 末尾的'/'（如果有），作为最后一个key
        3. 中间以'/'分隔

        eg:
            /a/b/c/:x/
        =>
            ['/', 'a', 'b', 'c', ':x', '/']
        """
        if not path or path[0] != '/':
            raise Exception(f"invalid path: {path}")

        # 去掉头尾的'/'
        tmp = path.strip('/')

        keys = []
        if tmp:
            keys = tmp.split('/')

        keys.insert(0, '/')

        if path.endswith('/') and path != '/':
            keys.append('/')

        # print(f"path: {path}, keys: {keys}")
        return keys

    @staticmethod
    def is_static_route(path):
        """判断是否是静态路由"""
        if ('*' not in path) and (':' not in path):
            # 路由中不包含`*`和`:`
            return True

        return False

    @staticmethod
    def _insert_remained(node, keys):
        """把路径的剩余部分keys也加入到tree中"""
        # todo: debug
        # print('cur:', node, 'remain:', keys)
        if not keys:
            return

        for key in keys:
            new = Node(key=key)
            node.add_child(new)
            node = new

        return node

    def insert(self, path: str, handler):
        """插入一个路由到树中"""
        if self.is_static_route(path):
            # 静态路由，直接加入dict中
            self._map[path] = handler
            return True

        keys = self.path_to_keys(path)

        cur = self._root
        for i, key in enumerate(keys):
            child = cur.find_child(key)       # found: Node
            if not child:
                last = self._insert_remained(cur, keys[i:])
                last.handler = handler
                return True
            else:
                cur = child

        cur.handler = handler
        return True

    def search(self, path):
        """
        把path按'/'分为多个key
        每个key中tree中进行匹配，查找handler，且分析出动态url中的参数(params)
        有3种情况：
        1. key全匹配
        2. `:`匹配
        route: `/a/b/c/:userId`
        path:  `/a/b/c/11`
        =>
        params: { 'userId': '11' }

        3. `*`匹配
        route: `/a/b/c/d/*y`
        path:  `/a/b/c/d/222/333`
        =>
        params: { 'y': '222/333' }
        """
        params = {}

        if not path:
            return None, params

        # 如果在 self._map 中找到匹配的静态路由，直接返回
        handler = self._map.get(path, None)
        if handler is not None:
            n = Node()
            n.path = path
            n.handler = handler
            return n, params

        keys = self.path_to_keys(path)

        cur = self._root
        for i, key in enumerate(keys):
            child = cur.find_child(key)
            # 如果都不完全匹配子节点
            if not child:
                # 如果子节点中也没有通配符节点，则说明没有相应的handler，直接返回
                if not cur.wildcard_child:
                    return None, params
                else:
                    # 如果有通配符，按通配符规则匹配
                    cur = cur.wildcard_child
                    if cur.key.startswith(':'):

                        # 最后的key是'/'时，不能算匹配通配符
                        # 否则，`/user/` 会匹配： `/user/:id`
                        if key == '/':
                            return None, params

                        # 匹配单个key的值，把节点中的key作为参数的键，url中的key作为参数值，最后返回给handler
                        # 继续往下匹配
                        params.update({
                            cur.key[1:]: key        # cur.key[1:], 去掉前面的`:`
                        })

                    elif cur.key.startswith('*'):
                        # `*`匹配剩余所有key
                        remained = keys[i:]     # 剩余部分的path全部作为参数返回
                        if remained:
                            remained = '/'.join(remained)

                        params.update({cur.key[1:]: remained})
                        return cur, params
            else:
                cur = child

        return cur, params

    def _print_node(self, node, depth):
        """递归展示某个节点及其子节点"""
        if not node.children:
            return

        print(' ' * depth, node.children)

        for child in node.children:
            self._print_node(child, depth + 1)

    def print_dynamic_routes(self):
        """展示所有动态路由（树的形式）"""
        print()
        print("dynamic routes:")
        self._print_node(self._root, 0)

    def print_static_routes(self):
        """展示所有静态路由（url形式）"""
        print()
        print("static routes:")
        for path in self._map.keys():
            print(' ', path)

    def _find_handler_node(self, node: Node, routes: dict):
        """找到有handler的节点"""
        if not node.children:
            return

        for child in node.children:
            if child.handler is not None:
                routes[child.path] = child.handler
            self._find_handler_node(child, routes)

    def print_all_routes(self):
        """展示全部路由（url形式）"""
        print()
        print("all routes:")
        routes = {}
        self._find_handler_node(self._root, routes)

        routes.update(self._map)

        if routes:
            for r in sorted(routes.keys()):
                print(' ', r)


########################################################################
# test
########################################################################


class CheckRequest(object):
    def __init__(self, path, route, handler, args):
        self.path = path
        self.route = route
        self.handler = handler
        self.args = args


def fake_handler(route):
    def _echo():
        print(f"route in handler: {route}")
        return route

    return _echo


def fake_handler2(route):
    def _echo2():
        print(f"route in handler: {route}")
        return route

    return _echo2


def _test():

    tree = Tree()

    routes = [
        '/',
        '/a/b/c',
        '/a/b/c/:x',
        '/a/b/c/:x/',
        '/a/b/c/:x/:z',
        '/a/b/c/d',
        # '/a/b/c/*w',
        # '/a/b/c/:w',
        '/a/b/c/d/*y',
        '/c',
    ]

    for route in routes:
        tree.insert(route, fake_handler(route))

    r = '/c'
    tree.insert(r, fake_handler2(r))

    tree.print_all_routes()
    tree.print_static_routes()
    tree.print_dynamic_routes()

    routes = [
        '/',
        '/c',
        '/d',
        '/a/b/c',
        '/a/b/:x',
        '/a/b/c/d',
        '/a/b/c/11',
        '/a/b/c/11/',
        '/a/b/c/11/22',
        '/a/b/c/d/222/333',
        '/a/b/c/d/222-333',
    ]

    print()
    for path in routes:
        print('-' * 20)
        node, params = tree.search(path)
        print(f"url: {path}, node: {node}, var: {params}")
        if node:
            route, handler = node.path, node.handler
            print(f"route: {route}, handler: {handler.__name__}")
            print(f"path == route ? {route == handler()}")

        print()


if __name__ == "__main__":
    _test()
