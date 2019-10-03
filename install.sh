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

function install_all_without_conf() {
    install_yonder_nginx
    install_yonder_frontend
    install_yonder_server_go
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
    config)
        install_go_config
        ;;
    backup)
        install_backup
        ;;
    all)
        install_all_without_conf
        ;;
    *)
        echo "$0 {nginx|vue|go|config|backup|all}" 
        exit 1
        ;;
esac
