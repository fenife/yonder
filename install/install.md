# 本地开发与远程部署
系统：
```shell script
$ cat /etc/os-release
NAME="Ubuntu"
VERSION="18.04.3 LTS (Bionic Beaver)"
ID=ubuntu
ID_LIKE=debian
```

## 准备（每个环境都要）
### 安装mysql
```shell script
$ sudo apt update
$ sudo apt install mysql-server

$ apt show mysql-server
Package: mysql-server
Version: 5.7.29-0ubuntu0.18.04.1
...
```

```shell script
# root用户配置变更
$ sudo mysql
> SELECT user,authentication_string,plugin,host FROM mysql.user;
> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
> FLUSH PRIVILEGES;
> exit
```

```shell script
# 创建test用户
$ mysql -u root -p
Enter password: root
> CREATE USER 'test'@'localhost' IDENTIFIED BY 'test';
> GRANT ALL PRIVILEGES ON test.* TO 'test'@'localhost' WITH GRANT OPTION;
> FLUSH PRIVILEGES;
> exit

# 验证test用户是否创建成功
$ mysql -u test -p
```

ref: 
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04

### 安装redis 

```shell script
$ sudo apt install redis-server
$ apt show redis-server
Package: redis-server
Version: 5:4.0.9-1ubuntu0.2
...
```

检查是否安装成功，后续用默认的端口(6379)即可
```shell script
$ redis-cli -h 127.0.0.1 -p 6379
127.0.0.1:6379>
```

ref:
https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04

### 安装nodejs和npm
```shell script
$ sudo apt install nodejs
$ sudo apt install npm
$ node -v
v8.10.0

$ npm -v
3.5.2
```

### 安装依赖库文件
```shell script
$ sudo apt-get install libmysqlclient-dev
```

ref:
https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-18-04
    
## 本地开发 (dev)
### 安装pip3
```shell script
$ python3 -V
Python 3.6.8

$ sudo apt install -y python3-pip
$ pip3 -V
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
```

添加pip源，加快下载速度，在`~/.pip/pip.conf`文件中加入以下内容：
```shell script
[global]
index-url=http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
```

如果`~/.pip/pip.conf`文件不存在则手动创建：
```shell script
$ mkdir ~/.pip
$ vi ~/.pip/pip.conf
```

### 安装virtuanenv    
安装virtualenv
```shell script
$ sudo apt install virtualenv
$ apt show virtualenv
Package: virtualenv
Version: 15.1.0+ds-1.1
...
```

创建一个独立的Python运行环境，命名为`venv`：
```shell script
$ cd <workdir>
$ virtualenv venv --python=python3
```

### 安装第三方包
```shell script
# 激活venv环境
$ source venv/bin/activate

# 安装某个包
$ pip3 install redis==3.3.11

# 退出当前的venv环境
$ deactivate
```

ref:
https://www.liaoxuefeng.com/wiki/1016959663602400/1019273143120480

### 启动服务
1. 配置文件
进入`yonder/etc/server`目录，编辑好`yonder_dev.py`配置文件后，
执行：`make dev`生成json文件

2. 启动python后端
```shell script
$ cd /icode/yonder/src/server_py3/aps/src
$ python main.py
```

3. 启动go后端
```shell script
$ cd /icode/yonder/src/server_go
$ go run main.go
```

4. 启动vue前端
```shell script
$ cd /icode/yonder/src/frontend_vue
$ npm run dev
```

## 远程部署(test)
### 安装supervisor (后端服务进程管理)
```shell script
$ sudo apt-get install supervisor
$ apt show supervisor
Package: supervisor
Version: 3.3.1-1.1
...
```

在`/etc/supervisor/conf.d/`中添加一个`app`的配置文件，启动服务：
```shell script
$ sudo supervisorctl reload
$ sudo supervisorctl start <app>
$ sudo supervisorctl status
```

ref:
https://www.liaoxuefeng.com/wiki/1016959663602400/1018491264935776

### 安装pm2 (前端服务进程管理)
```shell script
$ sudo npm install -g cnpm --registry=https://registry.npm.taobao.org
$ sudo cnpm install -g pm2
```

相关命令：
```shell script
$ pm2 list|start|restart|stop
$ cd <frontend_workdir>
$ pm2 start npm --name "<app_name>" -- run start
```

### 安装nginx
```shell script
$ sudo apt install nginx
$ apt show nginx
Package: nginx
Version: 1.14.0-0ubuntu1.7
...
```

### 部署
进入`yonder/etc/server`目录，编辑好`yonder_test.py`配置文件

进入`yonder/install`目录，
编辑`_deploy_env`行，选择部署环境：`test`或者`live` 

然后执行：
```shell script
# 看有那些需要部署的内容
$ fab -l

# 准备工作目录
fab prepare 

# 备份远程数据库到本地
fab backup

# 部署配置文件
$ fab etc

# 部署python后端
$ fab pip
$ fab py3

# 部署golang后端
$ fab go

# 部署vue前端
$ fab vue

# 部署nginx
# 进入`yonder/etc/nginx`目录，
# 编辑`server_name`行，设置要监听的域名或ip
$ fab nginx
```

添加域名-ip的映射到`/etc/hosts/`文件中
域名： nginx中`server_name`对应的监听域名
ip：  服务器ip
比如：
`192.168.0.10	test.yonder.com`
然后在浏览器通过`test.yonder.com`域名即可访问博客

## 远程部署(live)

