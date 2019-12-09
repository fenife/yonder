#!/usr/bin/env python3

from test_app import cache_pool

from sim.pretty import dictList2Table


def test():
    with cache_pool.get() as cache:
        cache.set('hello', 'app')
        print(cache.get('hello'))


if __name__ == "__main__":
    test()
