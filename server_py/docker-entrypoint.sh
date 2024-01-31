#!/bin/bash

# 数据表更新
python3 /yonder/server_py/migrate.py all

# 创建默认管理员 
python3 /yonder/server_py/main.py admin

# 启动服务
python3 /yonder/server_py/main.py

