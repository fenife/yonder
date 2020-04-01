#!/usr/bin/env python3

"""
将配置文件转换为json文件
"""

import json

with open('./yonder.conf', 'r') as f:
    conf = eval(f.read())   # 转换为dict

with open('./yonder.json', 'w') as f:
    json.dump(conf, f, ensure_ascii=False, indent=2)
