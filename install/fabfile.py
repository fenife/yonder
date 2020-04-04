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
    deploy etc conf
    move nginx config and supervisor config to yonder/etc/
    deploy golang

## todo
    restore backup data to remote mysql
"""

import os
import sys
import json
import datetime
import collections
import pprint

# 导入Fabric API:
from fabric.api import *

# 要部署到哪个环境 (test,live)
# 此变量对应配置文件的后缀
# `dev`一般为本地开发环境，不需要远程部署
_deploy_env = 'test'

# 本地相关目录
# ./../
_local_base_dir   = os.path.abspath(os.path.abspath(__file__).split('/install', 1)[0])
_local_src_dir    = os.path.join(_local_base_dir, 'src')
_local_build_dir  = os.path.join(_local_base_dir, 'build')
_local_backup_dir = os.path.join(_local_base_dir, 'backup')
_local_etc_dir = os.path.join(_local_base_dir, 'etc')
_local_etc_server_dir = os.path.join(_local_etc_dir, 'server')

# 读取配置文件
_conf_pyfile = f"yonder_{_deploy_env}.py"
_conf_json   = f"yonder_{_deploy_env}.json"
with lcd(f"{_local_etc_server_dir}"):
    local(f"python3 {_conf_pyfile}")    # 生成json文件
    with open(f"{_local_etc_server_dir}/{_conf_json}", 'r') as f:
        conf = json.load(f)

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
    "conf file": f"{_local_etc_server_dir}/{_conf_pyfile}",
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


def _remote_os_exist(path):
    result = run(f" [ -e '{path}' ] && echo 1 || echo 0")
    exist = int(result.stdout.strip('\n'))
    return exist


def _check_remote_path(path):
    # result = run(f" [ -e '{path}' ] && echo 1 || echo 0")
    # exist = int(result.stdout.strip('\n'))
    exist = _remote_os_exist(path)
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
    _py_file = "server_py3"
    _tar_py_file = f"{_py_file}.tar.gz"
    _local_py_dir = f"{_local_src_dir}/{_py_file}"

    _remote_py_dir = f"{_remote_src_dir}/{_py_file}"
    _remote_tar_py_file = f"{_remote_src_dir}/{_tar_py_file}"

    _remote_tmp_py_file = f'/tmp/{_tar_py_file}'

    # _prepare_path()
    _check_remote_path(_remote_log_dir)
    _check_remote_path(_remote_py_dir)

    # 打包
    excludes = ['data', 'logs', '*.log', '*.pyc', '*.pyo', '*__pycache__*']
    with lcd(_local_src_dir):
        cmd = ["tar", "-czf", f"{_local_build_dir}/{_tar_py_file}"]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend([f"{_py_file}"])
        local(' '.join(cmd))

    # 删除
    if _remote_os_exist(_remote_tar_py_file):
        run(f"rm -rf {_remote_tar_py_file}")

    # 把本地打包好的python代码上传到服务器
    put(f"{_local_build_dir}/{_tar_py_file}", f"{_remote_tar_py_file}")

    _remote_bak_py_dir = f"{_remote_py_dir}_bak"
    with cd(_remote_src_dir):
        # 删除旧的备份文件
        if _remote_os_exist(_remote_bak_py_dir):
            run(f"rm -rf {_remote_bak_py_dir}")

        # 重命名、备份原来的代码
        if _remote_os_exist(_remote_py_dir):
            run(f"mv {_remote_py_dir} {_remote_bak_py_dir}")

        # run(f"mkdir {_remote_py_dir}")

    # 解压
    with cd(_remote_src_dir):
        run(f"tar -xzf {_remote_tar_py_file}")

    # 上传 supervisor conf 文件
    # _spv_for('py3')

    # 重启服务
    with settings(warn_only=True):
        sudo('supervisorctl restart server_py3')
        # sudo('supervisorctl stop server_py3')
        # sudo('/etc/init.d/nginx reload')


########################################
# supervisor
########################################

_remote_spv_log_dir = f"{_remote_log_dir}/supervisor"
_remote_spv_dir = f"{_remote_etc_dir}/supervisor"

_tar_spv_file = f"supervisor.tar.gz"

_local_spv_dir = f"{_local_etc_dir}/supervisor"


def _spv_for(srv):
    """
    supervisor config for one server
    :param srv: py3/go
    :return:
    """
    _check_remote_path(_remote_spv_log_dir)
    _check_remote_path(_remote_spv_dir)

    _spv_conf_file = f"server_{srv}.conf"

    # 上传到 yonder/etc/supervisor
    put(f"{_local_spv_dir}/{_spv_conf_file}", f"{_remote_spv_dir}/{_spv_conf_file}")

    # 复制
    with cd(_remote_spv_dir):
        sudo(f"cp {_spv_conf_file} /etc/supervisor/conf.d/")

    sudo(f"supervisorctl reload")
    # sudo(f"sudo supervisorctl restart server_py3")
    sudo(f"supervisorctl status")


def spv():
    """
    all supervisor config
    """

    _check_remote_path(_remote_spv_log_dir)
    _check_remote_path(_remote_spv_dir)

    # 上传到 yonder/etc/supervisor
    with lcd(_local_spv_dir):
        files = os.listdir(_local_spv_dir)
        for fn in files:
            put(f"{_local_spv_dir}/{fn}", f"{_remote_spv_dir}/{fn}")

    # 复制
    with cd(_remote_spv_dir):
        sudo(f"cp ./* /etc/supervisor/conf.d/")

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

    with cd(_remote_vue_dir):
        # 解压
        run(f"tar -xzf {_remote_tar_vue_file}")
        run(f"npm install")
        run(f"npm run build")

    with settings(warn_only=True):
        # 必须进入package.json所在的目录再用pm2重启，否则启动的不是我们想要的进程
        with cd(_remote_vue_dir):
            # 重启
            # 这里的frontend_vue要跟第一次启动vue项目的名称一致
            run(f"pm2 stop frontend_vue")
            run(f"pm2 delete frontend_vue")
            run(f'pm2 start npm --name "frontend_vue" -- run start')


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
    _remote_etc_server_dir = f"{_remote_etc_dir}/server"

    _check_remote_path(_remote_etc_server_dir)

    # 上传到 yonder/etc
    put(f"{_local_etc_server_dir}/{_conf_pyfile}", f"{_remote_etc_server_dir}/{_conf_pyfile}")
    put(f"{_local_etc_server_dir}/Makefile", f"{_remote_etc_server_dir}/Makefile")

    # 生成json配置并重命名
    with cd(_remote_etc_server_dir):
        run(f"make {_deploy_env}")


########################################
# golang
########################################

def go():
    """
    server_go
    """
    _go_execute_file = "yonder_server_go"
    _tar_go_execute_file = f"{_go_execute_file}.tar.gz"

    _remote_go_dir = f"{_remote_src_dir}/server_go"
    _remote_tar_go_file = f'{_remote_go_dir}/{_tar_go_execute_file}'
    _remote_go_exe_file = f"{_remote_go_dir}/{_go_execute_file}"

    _check_remote_path(_remote_go_dir)

    # 压缩到 build/
    with lcd(os.path.join(_local_src_dir, 'server_go')):
        # build
        local("make build-linux")
        # tar
        cmd = ["tar", "-czvf", f"{_local_build_dir}/{_tar_go_execute_file}"]
        cmd.extend([_go_execute_file])
        local(' '.join(cmd))

    # 删除
    run(f"rm -rf {_remote_tar_go_file}")

    # 上传
    put(f"{_local_build_dir}/{_tar_go_execute_file}", _remote_tar_go_file)

    _remote_bak_go_exe_file = f"{_remote_go_exe_file}_bak"
    with cd(_remote_go_dir):
        # 删除旧的备份文件
        if _remote_os_exist(_remote_bak_go_exe_file):
            run(f"rm -rf {_remote_bak_go_exe_file}")

        # 重命名、备份原来的代码
        if _remote_os_exist(_remote_go_exe_file):
            run(f"mv {_remote_go_exe_file} {_remote_bak_go_exe_file}")

        # 解压
        run(f"tar -xzf {_remote_tar_go_file}")

    # 上传 supervisor conf 文件
    _spv_for('go')

    # 重启服务
    with settings(warn_only=True):
        sudo('supervisorctl restart server_go')
        # sudo('supervisorctl stop server_py3')
        # sudo('/etc/init.d/nginx reload')
