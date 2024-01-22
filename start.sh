#!/bin/bash

YONDER_DATA_DIR=/var/yonder/mysql
YONDER_LOG_DIR=/var/yonder/logs

set -x

if [ ! -d ${YONDER_DATA_DIR} ]; then
    mkdir ${YONDER_DATA_DIR} -p
fi

if [ ! -d ${YONDER_LOG_DIR} ]; then
    mkdir ${YONDER_LOG_DIR} -p
fi

