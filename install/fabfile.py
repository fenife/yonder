#!/usr/bin/env python3

"""
usage:
1. settep YONDER_CONFIG
    export YONDER_CONFIG=dev
    or:
    export YONDER_CONFIG=live

2. deploy, see:
    fab -l

todo:
## support
    export YONDER_CONFIG=dev
    or:
    export YONDER_CONFIG=live

## install supervisor and start server

## deploy vue

## deploy nginx

## deploy golang

## restore backup data to local mysql

## restore backup data to remote mysql
"""

import os
import re
import datetime

# 导入Fabric API:
from fabric.api import *

# 服务器地址，可以有多个，依次部署:
env.hosts = ['192.168.0.107']
# 服务器登录用户名:
env.user = 'feng'
# sudo用户为root:
env.sudo_user = 'root'

_db_user = "test"
_db_password = "test"
_db_name = "test"

# 远程相关目录
_remote_base_dir = "/icode/yonder"
_remote_log_dir = os.path.join(_remote_base_dir, 'logs')
_remote_src_dir = os.path.join(_remote_base_dir, 'src')

# 打包的python代码文件
_pyfile = "server_py3"
_tar_pyfile = f"{_pyfile}.tar.gz"
_remote_tmp_pyfile = f'/tmp/{_tar_pyfile}'

# 本地相关目录
_local_base_dir = os.path.abspath('..')
_local_src_dir = os.path.join(_local_base_dir, 'src')
_local_build_dir = os.path.join(_local_base_dir, 'build')
_local_backup_dir = os.path.join(_local_base_dir, 'backup')

print(_remote_log_dir)
print(_local_build_dir)
print(_local_backup_dir)


def _now():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')


def _check_remote_path(path):
    result = run(f" [ -e '{path}' ] && echo 1 || echo 0")
    exist = int(result.stdout.strip('\n'))
    if not exist:
        print(f"[remote] `{path}` not exists, create it")
        sudo(f"mkdir -p {path}")
        sudo(f"chown -R {env.user}:{env.user} {path}")
    else:
        print(f"[remote] `{path}` exists\n")


def _prepare_path():
    """
    准备工作目录
    :return:
    """
    with cd('/'):
        _check_remote_path(_remote_log_dir)
        _check_remote_path(_remote_src_dir)


def _check_local_path(path):
    if not os.path.exists(path):
        print(f"mkdirs: {path}")
        os.makedirs(path)


########################################
# backup data
########################################

def backup():
    """
    备份数据库，下载到本地
    """
    dt = _now()
    fn = f"backup-yonder-{dt}.sql"
    target = f"{fn}.tar.gz"

    with cd('/tmp'):
        cmd = f"mysqldump --user={_db_user} --password={_db_password} " \
              f"--skip-opt --add-drop-table --default-character-set=utf8 " \
              f"--quick {_db_name} > {fn}"
        run(cmd)
        run(f"tar -czvf {target} {fn}")
        # 下载到本地的备份目录(_local_backup_dir)中
        get(target, _local_backup_dir)
        run(f"rm -f {fn}")
        run(f"rm -f {target}")


########################################
# Python server
########################################

def _build_py3():
    # _prepare_path()

    excludes = ['data', 'logs', '*.log', '*.pyc', '*.pyo', '*__pycache__*']

    with lcd(os.path.join(_local_base_dir, 'src', 'server_py3')):
        cmd = ["tar", "-czf", f"{_local_build_dir}/{_tar_pyfile}"]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(['.'])
        local(' '.join(cmd))


def py3():
    """
    server_py3
    """
    _prepare_path()

    _build_py3()

    newdir = f"{_pyfile}-{_now()}"
    run(f"rm -f {_remote_tmp_pyfile}")
    # 把本地打包好的python代码上传到服务器
    put(f"{_local_build_dir}/{_tar_pyfile}", _remote_tmp_pyfile)

    with cd(_remote_src_dir):
        run(f"mkdir {newdir}")

    with cd(f"{_remote_src_dir}/{newdir}"):
        run(f"tar -xzf {_remote_tmp_pyfile}")

    with cd(_remote_src_dir):
        run(f"rm -f {_pyfile}")
        run(f"ln -s {newdir} {_pyfile}")

    with settings(warn_only=True):
        sudo('supervisorctl restart server_py3')
        # sudo('supervisorctl stop server_py3')
        # sudo('/etc/init.d/nginx reload')


########################################
# supervisor
########################################

def spv():
    """
    supervisor config
    """
    _check_remote_path(f"{_remote_log_dir}/supervisor/")
    _remote_tmp_supervisor_conf = '/tmp/yonder.conf'
    with cd('/tmp/'):
        put(f"{_local_src_dir}/supervisor/yonder.conf", _remote_tmp_supervisor_conf)
        sudo(f"cp {_remote_tmp_supervisor_conf} /etc/supervisor/conf.d/")
        sudo(f"supervisorctl reload")


########################################
# 前端
########################################

def vue():
    """
    frontend_vue
    """
    _remote_vue_dir = f"{_remote_src_dir}/frontend_vue"
    _check_remote_path(_remote_vue_dir)

    # 压缩到build/
    # 上传
    # 解压
    # npm build
    # pm2 start


########################################
# nginx
########################################

def nginx():
    """
    nginx config
    """


########################################
# golang
########################################

def go():
    """
    server_go
    """
