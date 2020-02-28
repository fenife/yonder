#!/bin/bash

# only in ubuntu

# before run this shell
# mkdir /work
# chown <user>:<user> /work
# cd /work
# git clone https://github.com/kfrime/yonder.git
# edit yonder_server_go/config.example.json


echo "edit mysql config of 'yonder/data_backup/sh/backup.sh' first"
echo "edit config of 'yonder/server_go/config.example.json' first"
echo "edit yonder/nginx/nginx.example.conf config, listen server ip in nginx"

set -x

# root dir
WORK_HOME=/work
LOG_HOME=${WORK_HOME}/logs/yonder
PROJECT_DIR=${WORK_HOME}/yonder

# nginx
NGINX_CONF=${PROJECT_DIR}/nginx
LOG_NGINX=${LOG_HOME}/nginx

function install_yonder_nginx() {
    echo "start nginx ..."

    if [ ! -d ${LOG_NGINX} ]; then
    mkdir ${LOG_NGINX} -p
    fi

    sudo cp ${NGINX_CONF}/nginx.example.conf /etc/nginx/conf.d/yonder.conf
    echo "edit /etc/nginx/conf.d/yonder.conf, listen server ip in nginx"
    sudo nginx -t
    sudo nginx -s reload
    ps aux | grep nginx
}

# yonder_frontend_vue
WORK_FRONTEND=${PROJECT_DIR}/frontend_vue

function install_yonder_frontend() {
    echo "start frontend ..."

    cd ${WORK_FRONTEND}
    sudo kill -9 $(ps aux | grep 'yonder_frontend_vue' | grep -v grep | awk '{print $2}')
    npm i
    sudo npm run build
    sudo npm run start & > /dev/null 2>&1
    ps aux | grep yonder_frontend_vue | grep -v grep 
}

# yonder_server_go
WORK_SERVER_GO=${PROJECT_DIR}/server_go
LOG_SERVER_GO=${LOG_HOME}/server_go

function install_yonder_server_go() {
    echo "start server ... "

    if [ ! -d ${LOG_SERVER_GO} ]; then
        mkdir ${LOG_SERVER_GO} -p
    fi

    if [ ! -f ${LOG_SERVER_GO}/server.log ]; then 
        touch ${LOG_SERVER_GO}/server.log
    fi

    cd ${WORK_SERVER_GO}
    sudo kill -9 $(ps aux | grep 'yonder_server_go' | grep -v grep | awk '{print $2}')
    # cp ${WORK_SERVER_GO}/config.example.json ${WORK_SERVER_GO}/config.json
    sudo ./yonder_server_go & > /dev/null 2>&1

    ps aux | grep yonder_server_go | grep -v grep 
}

function install_go_config() {
    cp ${WORK_SERVER_GO}/config.example.json ${WORK_SERVER_GO}/config.json
}

# data backup
BACKUP_SCRIPT=${PROJECT_DIR}/data_backup
BACKUP_DIR=${WORK_HOME}/backup

function install_backup() {
    echo "install backup script ..."

    if [ ! -d ${BACKUP_DIR} ]; then
        mkdir ${BACKUP_DIR}
    fi

    sudo cp ${BACKUP_SCRIPT}/backup.cron  /etc/cron.d

    ls /etc/cron.d/
}


# server_py3
# export PYTHONPATH=$PYTHONPATH:/work/yonder/server_py3/sim
# export YONDER_CONFIG=live
# cd /work/yonder/server_py3/aps/wes/config
# cp config_dev.py config_live.py
# vi config_live.py
# cd /work/yonder/server_py3/
# python3 migrate.py all
# python3 main.py admin


WORK_SERVER_PY3=${PROJECT_DIR}/server_py3
LOG_SERVER_PY3=${LOG_HOME}/server_py3

function install_yonder_server_py3() {
    echo ''
    echo "copy and edit config_live.py first"
    echo ''
    sleep 0.5

    export PYTHONPATH=$PYTHONPATH:${WORK_SERVER_PY3}/sim
    echo $PYTHONPATH

    echo "export YONDER_CONFIG=live"
    export YONDER_CONFIG=live

    echo "start server py3 ... "

    if [ ! -d ${LOG_SERVER_PY3} ]; then
        mkdir ${LOG_SERVER_PY3} -p
    fi

    if [ ! -f ${LOG_SERVER_PY3}/app.log ]; then
        touch ${LOG_SERVER_PY3}/app.log
    fi

    cd ${WORK_SERVER_PY3}
    pid=$(ps aux | grep 'aps/main.py' | grep -v grep | awk '{print $2}')
    if [ -n "${pid}" ]; then
        echo "${pid}" | xargs sudo kill -9
    fi

    python3 ${WORK_SERVER_PY3}/aps/main.py & > /dev/null 2>&1

    ps aux | grep "aps/main.py" | grep -v grep
}

# search service
# /work/yonder/server_py3/search
# cd /work/yonder/server_py3/aps/wes/config
# cp config_dev.py config_live.py
# vi config_live.py
# cd /work/yonder/server_py3/
# python3 migrate.py all
# python3 main.py admin


SEARCH_HOME=${PROJECT_DIR}/server_py3/search
SEARCH_LOG=${SEARCH_HOME}/logs
SEARCH_DATA=${SEARCH_HOME}/data

function install_yonder_search_service() {
    echo ''
    echo "copy and edit config_live.py first"
    echo ''
    sleep 0.5

    export PYTHONPATH=$PYTHONPATH:${WORK_SERVER_PY3}/sim
    echo $PYTHONPATH

    echo "export YONDER_CONFIG=live"
    export YONDER_CONFIG=live

    echo "start search service ... "

    if [ ! -d ${SEARCH_LOG} ]; then
        mkdir ${SEARCH_LOG} -p
    fi

    if [ ! -d ${SEARCH_DATA} ]; then
        mkdir ${SEARCH_DATA} -p
    fi

    cd ${SEARCH_HOME}/src
    pid=$(ps aux | grep 'ses/main.py' | grep -v grep | awk '{print $2}')
    if [ -n "${pid}" ]; then
        echo "${pid}" | xargs sudo kill -9
    fi

    python3 ${SEARCH_HOME}/src/main.py & > /dev/null 2>&1

    ps aux | grep "search/src/main.py" | grep -v grep
}

function install_all_without_conf() {
    install_yonder_nginx
    install_yonder_frontend
    install_yonder_server_go
    install_yonder_server_py3
    # install_go_config
    install_backup
}


case $1 in
    nginx)
        install_yonder_nginx
        ;;
    vue)
        install_yonder_frontend
        ;;
    go)
        install_yonder_server_go
        ;;
    config_go)
        install_go_config
        ;;
    py3)
        install_yonder_server_py3
        ;;
    backup)
        install_backup
        ;;
    search)
        install_yonder_search_service
        ;;
    all)
        install_all_without_conf
        ;;
    *)
        echo "$0 {nginx|vue|go|config_go|py3|backup|search|all}"
        exit 1
        ;;
esac
