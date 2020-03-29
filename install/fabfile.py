#!/usr/bin/env python3

"""
usage:
1. settep YONDER_CONFIG
    export YONDER_CONFIG=dev
    or:
    export YONDER_CONFIG=live

2. deploy, see:
    fab -l

## done
    install supervisor and start server
    vue
    nginx
    restore backup data to local mysql

## todo
1.
    export YONDER_CONFIG=dev
    or:
    export YONDER_CONFIG=live

2. deploy golang
3. restore backup data to remote mysql
4. deploy etc conf
5. move nginx config and supervisor config to yonder/etc/
"""

import os
import sys
import datetime
from collections import OrderedDict

# 导入Fabric API:
from fabric.api import *

# 本地相关目录
# ./../
_local_base_dir = os.path.abspath(os.path.abspath(__file__).split('/install', 1)[0])
_local_src_dir = os.path.join(_local_base_dir, 'src')
_local_build_dir = os.path.join(_local_base_dir, 'build')
_local_backup_dir = os.path.join(_local_base_dir, 'backup')

# todo: 根据变量读取相应的配置文件，部署到哪个环境？
_config_file = f"{_local_base_dir}/etc/server/yonder.conf"

# 读取配置文件
with open(_config_file, 'r') as f:
    conf = eval(f.read())

_debug_mode = True if conf.get('DEBUG_MODE') else False

# 远程相关目录
_remote_base_dir = "/icode/yonder"
_remote_log_dir = os.path.join(_remote_base_dir, 'logs')
_remote_src_dir = os.path.join(_remote_base_dir, 'src')

# 服务器地址，可以有多个，依次部署:
env.hosts = ['192.168.0.107']
# 服务器登录用户名:
env.user = 'feng'
# sudo用户为root:
env.sudo_user = 'root'

_db_user = "test"
_db_password = "test"
_db_name = "test"

# 打印部分选项
dct = OrderedDict({
    "conf file": _config_file,
    "env mode": conf.get('ENV_MODE'),
    'debug mode': _debug_mode,
    'local base dir': _local_base_dir,
    'remote base dir': _remote_base_dir,
})
_fl = max(map(len, dct.keys()))     # 为了左边对齐展示
print()
print('-' * 50)
for k, v in dct.items():
    print("{k:>{fl}} : {v}".format(fl=_fl, k=k, v=v))
print('-' * 50)
print()


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
    _remote_backup_dir = f"{_remote_base_dir}/backup"

    _check_remote_path(_remote_backup_dir)

    dt = _now()
    fn = f"backup-yonder-{dt}.sql"
    target = f"{fn}.tar.gz"

    with cd(_remote_backup_dir):
        cmd = f"mysqldump --user={_db_user} --password={_db_password} " \
              f"--skip-opt --add-drop-table --default-character-set=utf8 " \
              f"--quick {_db_name} > {fn}"
        run(cmd)
        run(f"tar -czvf {target} {fn}")
        # 下载到本地的备份目录(_local_backup_dir)中
        get(target, _local_backup_dir)
        run(f"rm -f {fn}")
        run(f"rm -f {target}")


def r2l():
    """
    restore database to local
    """
    fs = os.listdir(_local_backup_dir)
    files = [f for f in fs if f.startswith('backup-') and f.endswith('.sql.tar.gz')]
    files.sort(reverse=True)

    if not files:
        print('No backup files found.')
        return

    _restore_tar_file = files[0]
    _restore_file = _restore_tar_file.split('.tar.gz')[0]
    print(f"Start restore to local database, file: {_restore_tar_file}")
    sqls = [
        f"drop database if exists {_db_name};",
        f"create database {_db_name};",
    ]
    _mysql = f"mysql -u{_db_user} -p{_db_password} "
    for sql in sqls:
        local(f'{_mysql} -e "{sql}" ')

    with lcd(_local_backup_dir):
        local(f"tar -zxvf {_restore_tar_file}")

    # local(f"mysql -uroot -p%s awesome < backup/%s" % (p, restore_file[:-7]))
    local(f"{_mysql} {_db_name} < {_local_backup_dir}/{_restore_file}")
    with lcd(_local_backup_dir):
        local(f"rm -f {_restore_file}")


def restore2remote():
    """
    restore database to remote
    """

########################################
# Python server
########################################

def py3():
    """
    server_py3
    """
    # 打包的python代码文件
    _pyfile = "server_py3"
    _tar_pyfile = f"{_pyfile}.tar.gz"
    _remote_tmp_pyfile = f'/tmp/{_tar_pyfile}'

    _prepare_path()

    # 打包
    excludes = ['data', 'logs', '*.log', '*.pyc', '*.pyo', '*__pycache__*']
    with lcd(os.path.join(_local_base_dir, 'src', 'server_py3')):
        cmd = ["tar", "-czf", f"{_local_build_dir}/{_tar_pyfile}"]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(['.'])
        local(' '.join(cmd))

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
    _vue_file = "frontend_vue"
    _tar_vue_file = f"{_vue_file}.tar.gz"

    _remote_vue_dir = f"{_remote_src_dir}/frontend_vue"
    _remote_tar_vue_file = f'{_remote_src_dir}/{_tar_vue_file}'

    _check_remote_path(_remote_vue_dir)

    # 压缩到build/
    excludes = ['logs', '*.log', '.nuxt', 'node_modules']
    with lcd(os.path.join(_local_src_dir, 'frontend_vue')):
        cmd = ["tar", "-czf", f"{_local_build_dir}/{_tar_vue_file}"]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(['.'])
        local(' '.join(cmd))

    # 删除
    run(f"rm -rf {_remote_tar_vue_file}")

    # 上传
    put(f"{_local_build_dir}/{_tar_vue_file}", _remote_tar_vue_file)

    with cd(_remote_src_dir):
        # 删除旧的备份文件
        run(f"rm -rf {_remote_vue_dir}_bak")
        # 重命名、备份原来的代码
        run(f"mv {_remote_vue_dir} {_remote_vue_dir}_bak")
        # 新建文件夹
        run(f"mkdir {_remote_vue_dir}")

    with cd(f"{_remote_vue_dir}"):
        # 解压
        run(f"tar -xzf {_remote_tar_vue_file}")
        # run(f"npm install")
        run(f"npm run build")

    with settings(warn_only=True):
        # 重启
        # 这里的frontend_vue要跟第一次启动vue项目的名称一致
        run(f"pm2 restart frontend_vue")


########################################
# nginx
########################################

def nginx():
    """
    nginx config
    """
    _remote_nginx_log_dir = f"{_remote_log_dir}/nginx"
    _remote_nginx_dir = f"{_remote_src_dir}/nginx"
    _remote_nginx_conf = f"{_remote_nginx_dir}/yonder.conf"

    _local_nginx_conf = f"{_local_src_dir}/nginx/yonder.conf"

    _check_remote_path(_remote_nginx_log_dir)
    _check_remote_path(_remote_nginx_dir)

    # 上传到src/nginx
    put(_local_nginx_conf, _remote_nginx_conf)

    # 复制到etc
    with cd(_remote_nginx_dir):
        sudo(f"cp {_remote_nginx_conf} /etc/nginx/conf.d/yonder.conf")

    # 重启
    sudo("sudo nginx -t")
    sudo("sudo nginx -s reload")


########################################
# golang
########################################

def go():
    """
    server_go
    """
