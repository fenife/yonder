#!/usr/bin/env python3

"""
table or data migrate
"""


import sys

from wes.model import User, Category, Article


_opt2Model = {
    User.__table__:     User,
    Category.__table__: Category,
    Article.__table__:  Article,
}

opts = list(_opt2Model.keys()) + ['all']


def usage():
    print()
    print("usage: %prog [options]")
    print("  python migrate.py <table>")
    print(f"  python migrate.py {opts}")
    print()


def migrate_table(opt: str):
    t = _opt2Model.get(opt)
    tn = t.__table__
    reset = False
    if t.table_existed():
        print()
        print(f"table `{tn}` has been existed !!!")
        tip = f"are you sure to **drop** and recreate this table? <n|{tn}> [n] "
        i = input(tip)
        if i == tn:
            t.table_drop()
            reset = True

    else:
        reset = True

    if reset:
        t.table_create()
        t.table_show()
    else:
        print(f"nothing to do for table `{tn}`")

    print()


def main():
    try:
        opt = sys.argv[1]
    except Exception as e:
        print(str(e))
        usage()
        return

    if opt not in opts:
        print(f"expected options: {opts}, but get: {opt}")
        usage()
        return

    if opt == 'all':
        for opt, table in _opt2Model.items():
            migrate_table(opt)
    else:
        migrate_table(opt)


if __name__ == "__main__":
    main()
