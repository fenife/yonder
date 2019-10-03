#!/bin/bash

# 
# 数据恢复
# 

# Mysql数据库配置
HOST=localhost
PORT=3306
USER=root
PASSWORD=root
DB=yonder

# 备份目录
BACKUP_FILE=./${DB}_backup.sql

set -x

# 数据恢复命令
mysql -h${HOST} -P${PORT} -u${USER} -p${PASSWORD} -B ${DB} < ${BACKUP_FILE}
