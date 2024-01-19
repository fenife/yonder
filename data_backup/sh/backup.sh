#!/bin/bash

#
# 数据备份
# 

# Mysql数据库配置
HOST=localhost
PORT=3306
USER=root
PASSWORD=root
DB=yonder

# 备份目录
BACKUP_DIR=/work/backup
BACKUP_FILE=${BACKUP_DIR}/${DB}_backup.sql

# 创建目录
if [ ! -d ${BACKUP_DIR} ]; then
  mkdir ${BACKUP_DIR}
fi

set -x

# 备份命令
mysqldump -h${HOST} -P${PORT} -u${USER} -p${PASSWORD} -B ${DB} > ${BACKUP_FILE}
