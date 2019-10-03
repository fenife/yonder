# yonder
    server and frontend of yonder blog 

## blog_mini_server_go
    mini server of blog implemented by golang

## 依赖和准备
    系统以 ubuntu 16.04 为例
    1. mysql
    1.1 启动mysql
    service mysql start/restart/stop

    1.2 创建用户
    CREATE USER 'username'@'localhost' IDENTIFIED BY 'password'; 

    1.3 授权
    GRANT <privileges> ON databasename.tablename TO 'username'@'host'
    GRANT ALL ON *.* TO 'username'@'localhost';

    1.4 创建数据库
    create database <dbname>;

    2. redis
    1. 启动redis
    redis-server --port 6381 
    
    3. 启动后端服务
    /etc/nginx/conf.d


## 部署

    1. 创建配置文件，并填入个人密码等敏感信息
    `cp config.example.json config.json`
    
    2. 运行脚本
    `./run.sh`

    3. 启动nginx
    
    
## todo
    log 
    搜索(solr)
    Archive页
    数据库备份

## packages
    github.com/jinzhu/gorm
    github.com/gin-gonic/gin
    github.com/garyburd/redigo/redis

    // It protects sites from XSS attacks
    github.com/microcosm-cc/bluemonday

## changes
    connect to mysql
    connect to redis
    注册登陆
    分类CRUD
    文章CRUD
