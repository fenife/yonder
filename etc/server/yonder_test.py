#!/usr/bin/env python3

import json

conf = {
    # dev/live
    "ENV_MODE": "test",

    # 远程部署时ssh登陆的配置，密码在部署时会要求从命令行输入
    # /etc/hosts
    "SSH_HOSTS": ["192.168.0.107"],
    "SSH_USER": "feng",
    "SSH_SUDO_USER": "root",

    # app debug mode, 1: true; 0: false
    "DEBUG_MODE": 1,

    # database config
    "DB_HOST": "127.0.0.1",
    "DB_PORT": 3306,
    "DB_USER": "test",
    "DB_PASSWORD": "test",
    "DB_NAME": "test",
    "DB_CHARSET": "utf8",

    # cache/redis config
    "REDIS_HOST": "127.0.0.1",
    "REDIS_PORT": 6379,

    # app secret key to gen session token
    "SECRET_KEY": "a key hard to guess",

    # admin user for website
    "ADMIN_USERNAME": "admin",
    "ADMIN_PASSWORD": "admin",

    # page
    "PAGE_SIZE": 10,

    # 用户登录过期时间
    # login expired time (seconds)
    "LOGIN_EXPIRED": 1800,

    # log file path
    "LOG_PATH": "/icode/yonder/logs",

    # local backup database config
    "BACKUP_DB_HOST": "127.0.0.1",
    "BACKUP_DB_PORT": 3306,
    "BACKUP_DB_USER": "test",
    "BACKUP_DB_PASSWORD": "test",
    "BACKUP_DB_NAME": "test",
    "BACKUP_DB_CHARSET": "utf8"
}


if __name__ == "__main__":
    # 将配置文件转换为json文件
    with open('./yonder.json', 'w') as f:
        json.dump(conf, f, ensure_ascii=False, indent=2)
