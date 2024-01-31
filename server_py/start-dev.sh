#!/bin/bash

set -x 

# 数据表更新
# python3 /yonder/server_py/aps/src/migrate.py all

# 创建默认管理员 
# python3 /yonder/server_py/aps/src/main.py admin

# 启动服务
python3 /yonder/server_py/reloader.py /yonder/server_py/main.py


