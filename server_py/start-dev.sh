#!/bin/bash

set -x 

# 数据表更新
# python3 /yonder/server_py3/aps/src/migrate.py all

# 创建默认管理员 
# python3 /yonder/server_py3/aps/src/main.py admin

# 启动服务
python3 /yonder/server_py3/aps/src/reloader.py /yonder/server_py3/aps/src/main.py
# python3 /server_py3/aps/src/main.py


