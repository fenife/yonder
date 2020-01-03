#!/bin/sh
# description: Nginx Server

NGINX_HOME=/usr/local/openresty/nginx
NGINX_SBIN=$NGINX_HOME/sbin/nginx
NGINX_CONF=/work/yonder/server_openresty/ngx_conf/nginx.conf
NGINX_PID=/work/yonder/server_openresty/logs/nginx.pid

NGINX_NAME="yonder"

if [ ! -f $NGINX_SBIN ]
then
    echo "$NGINX_NAME startup: $NGINX_SBIN not exists! "
    exit
fi

start() {
    $NGINX_SBIN -c $NGINX_CONF
    ret=$?
    if [ $ret -eq 0 ]; then
        echo "Starting $NGINX_NAME: " /bin/true
    else
        echo "Starting $NGINX_NAME: " /bin/false
    fi
}

stop() {
    kill -TERM `cat $NGINX_PID`
    ret=$?
    if [ $ret -eq 0 ]; then
        echo "Stopping $NGINX_NAME: " /bin/true
    else
        echo "Stopping $NGINX_NAME: " /bin/false
    fi
}

restart() {
    stop
    sleep 0.5
    start
}

check() {
    $NGINX_SBIN -c $NGINX_CONF -t
}


reload() {
    kill -HUP `cat $NGINX_PID` && echo "reload success!"
}

relog() {
    kill -USR1 `cat $NGINX_PID` && echo "relog success!"
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    check|chk)
        check
        ;;
    status)
        status -p $NGINX_PID
        ;;
    reload)
        reload
        ;;
    relog)
        relog
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|reload|status|check|relog}"
        exit 1
esac