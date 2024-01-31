#!/usr/bin/env python3

from prettytable import PrettyTable


class LocalPrettyTable(PrettyTable):
    def rowLen(self):
        return len(self._rows)


def printListRows(header, rows, limit=50):
    """
    :param header: eg:
        (symbol, secu_type, third_class)
    :param rows: eg:
    (
        (u'hk00001', u'stock', u'010104'),
        (u'hk00002', u'stock', u'010104'),
    )

    :param limit: 打印多少行
    :return: eg:

    +---------+-----------+-------------+
    |  symbol | secu_type | third_class |
    +---------+-----------+-------------+
    | hk00001 |   stock   |    010104   |
    +---------+-----------+-------------+
    1 rows showed
    """
    # 按行添加数据
    # tb = PrettyTable()
    tb = LocalPrettyTable()
    tb.field_names = header
    for i, row in enumerate(rows):
        if i > limit-1:
            break

        tb.add_row(row)

    print(tb)
    print("{} rows showed\n".format(tb.rowLen()))


def printDictRows(header, rows, limit=50):
    """
    :param header: (symbol, secu_type, third_class)
    :param rows: eg:
    (
        {
            'symbol': u'hk00001',
            'third_class': u'010104',
            'secu_type': u'stock'
        },
        {...}, {...}, ...
    )

    :param limit: 打印多少行
    :return: eg:

    *************************** 1. row ***************************
         symbol: hk00001
    third_class: 010104
      secu_type: stock

    1 rows showed
    """
    width = max([len(f) for f in header])   # 获取最大字段长度
    fmt = "{k:>%s}: {v}" % (width, )        # 按最大长度，右对齐展示字段名称

    cnt = 0
    for i, row in enumerate(rows):
        print("*" * 27, "{i}. row".format(i=i+1), "*" * 27)
        for key, val in row.items():
            print(fmt.format(k=key, v=val))

        cnt = i+1       # i start from 0, need to add 1
        if i >= limit-1:
            break

    print("\n{} rows showed\n".format(cnt))


def dictList2Table(data, sort=False, limit=10):
    """
    :param data: 一个包含多个dict的list，各个dict的key必须一致
    [
        { '101': '阿里巴巴', '95': 'PRE', '1': 164.7, '0': 'nyBABA', '2': 161.93 },
        { '101': '苹果', '95': 'PRE', '1': 227.6, '0': 'oqAAPL', '2': 224.4 },
    ]
    :param limit:
    :return: table of :
        +--------+--------+--------+-----+----------+
        |   0    |   1    |   2    |  95 |   101    |
        +--------+--------+--------+-----+----------+
        | nyBABA | 164.62 | 165.19 | PRE | 阿里巴巴  |
        | oqAAPL | 227.81 | 227.03 | PRE |   苹果   |
        +--------+--------+--------+-----+----------+
    """

    if not data or type(data) not in (list, tuple):
        return

    header = data[0].keys()

    if sort:
        try:
            header = sorted(header, key=lambda x: int(x))   # 数字类型的话按数字大小排序
        except ValueError as e:
            header = sorted(header)     # 如果header包含非数字项，则按字母序排序

    rows = []
    for i, item in enumerate(data):
        row = [item.get(k) for k in header]
        rows.append(row)
        if i > limit - 1:
            break

    tb = LocalPrettyTable()
    tb.field_names = header
    for i, row in enumerate(rows):
        tb.add_row(row)

    return tb

