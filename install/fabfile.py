#!/usr/bin/env python3

"""
usage:
1. setup: _deploy_env=dev/live
2. fab -l

## done
    server_py3
    install supervisor and start server
    vue
    nginx
    restore backup data to local mysql
    setup deploy env

## todo
    deploy golang
    restore backup data to remote mysql
    deploy etc conf
    move nginx config and supervisor config to yonder/etc/
"""

import os
import sys
import datetime
import collections
import pprint

# 导入Fabric API:
from fabric.api import *

# 要部署到哪个环境 (dev,live)
_deploy_env = 'dev'

# 本地相关目录
# ./../
_local_base_dir   = os.path.abspath(os.path.abspath(__file__).split('/install', 1)[0])
_local_src_dir    = os.path.join(_local_base_dir, 'src')
_local_build_dir  = os.path.join(_local_base_dir, 'build')
_local_backup_dir = os.path.join(_local_base_dir, 'backup')
_local_etc_dir = os.path.join(_local_base_dir, 'etc')

# todo: 根据变量读取相应的配置文件，部署到哪个环境？
_server_config_file = f"{_local_base_dir}/etc/server/yonder_{_deploy_env}.conf"
# _local_conf_file    = f"{_local_base_dir}/etc/server/yonder.conf"

# 读取配置文件
with open(_server_config_file, 'r') as f:
    conf = eval(f.read())

# with open(_local_conf_file, 'r') as f:
#     lconf = eval(f.read())

_debug_mode = True if conf.get('DEBUG_MODE') else False

# 远程服务器的数据库配置
_remote_db_user     = conf.get('DB_USER')
_remote_db_password = conf.get('DB_PASSWORD')
_remote_db_name     = conf.get('DB_NAME')

# 本地的备份数据库配置
_backup_db_user      = conf.get('BACKUP_DB_USER')
_backup_db_password  = conf.get('BACKUP_DB_PASSWORD')
_backup_db_name      = conf.get('BACKUP_DB_NAME')

# 远程相关目录
_remote_base_dir = "/icode/yonder"
_remote_log_dir  = os.path.join(_remote_base_dir, 'logs')
_remote_src_dir  = os.path.join(_remote_base_dir, 'src')
_remote_etc_dir  = os.path.join(_remote_base_dir, 'etc')


# 服务器地址，可以有多个，依次部署:
env.hosts = conf.get('SSH_HOSTS')
# 服务器登录用户名:
env.user = conf.get('SSH_USER')
# sudo用户为root:
env.sudo_user = conf.get('SSH_SUDO_USER')

# pprint.pprint(conf)

# 打印部分选项
dct = collections.OrderedDict({
    "deploy env": _deploy_env,
    "env mode": conf.get('ENV_MODE'),
    "conf file": _server_config_file,
    # "conf file for local": _local_conf_file,
    'debug mode': _debug_mode,
    'local base dir': _local_base_dir,
    'remote base dir': _remote_base_dir,
    'ssh server host': env.hosts,
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
        cmd = f"mysqldump --user={_remote_db_user} --password={_remote_db_password} " \
              f"--skip-opt --add-drop-table --default-character-set=utf8 " \
              f"--quick {_remote_db_name} > {fn}"
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
        f"drop database if exists {_backup_db_name};",
        f"create database {_backup_db_name};",
    ]
    _mysql = f"mysql -u{_backup_db_user} -p{_backup_db_password} "
    for sql in sqls:
        local(f'{_mysql} -e "{sql}" ')

    with lcd(_local_backup_dir):
        local(f"tar -zxvf {_restore_tar_file}")

    # local(f"mysql -uroot -p%s awesome < backup/%s" % (p, restore_file[:-7]))
    local(f"{_mysql} {_backup_db_name} < {_local_backup_dir}/{_restore_file}")
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
    _remote_supervisor_log_dir = f"{_remote_log_dir}/supervisor"
    _remote_supervisor_dir = f"{_remote_etc_dir}/supervisor"
    _remote_supervisor_conf = f"{_remote_supervisor_dir}/yonder_supervisor.conf"

    _local_supervisor_conf = f"{_local_etc_dir}/supervisor/yonder_supervisor.conf"

    _check_remote_path(_remote_supervisor_log_dir)
    _check_remote_path(_remote_supervisor_dir)

    # 上传到 yonder/etc/supervisor
    put(_local_supervisor_conf, _remote_supervisor_conf)

    # 复制
    with cd(_remote_supervisor_dir):
        sudo(f"cp {_remote_supervisor_conf} /etc/supervisor/conf.d/")

    sudo(f"supervisorctl reload")
    # sudo(f"sudo supervisorctl restart server_py3")
    sudo(f"supervisorctl status")


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
    _remote_nginx_dir = f"{_remote_etc_dir}/nginx"
    _remote_nginx_conf = f"{_remote_nginx_dir}/yonder_nginx.conf"

    _local_nginx_conf = f"{_local_etc_dir}/nginx/yonder_nginx.conf"

    _check_remote_path(_remote_nginx_log_dir)
    _check_remote_path(_remote_nginx_dir)

    # 上传到src/nginx
    put(_local_nginx_conf, _remote_nginx_conf)

    # 复制到etc
    with cd(_remote_nginx_dir):
        sudo(f"cp {_remote_nginx_conf} /etc/nginx/conf.d/yonder_nginx.conf")

    # 重启
    sudo("sudo nginx -t")
    sudo("sudo nginx -s reload")


########################################
# etc config
########################################
def etc():
    """
    yonder etc server config
    """
    _local_etc_server_dir  = f"{_local_etc_dir}/server"
    _remote_etc_server_dir = f"{_remote_etc_dir}/server"
    _conf_file = f"yonder_{_deploy_env}.conf"

    _check_remote_path(_remote_etc_server_dir)

    # 上传到 yonder/etc
    put(f"{_local_etc_server_dir}/{_conf_file}", f"{_remote_etc_server_dir}/{_conf_file}")

    # 复制并重命名
    with cd(_remote_etc_server_dir):
        sudo(f"cp {_conf_file} yonder.conf")


########################################
# golang
########################################

def go():
    """
    server_go
    """
