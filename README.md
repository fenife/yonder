# yonder
搭建一个博客网站，实现了文章发布、标签分类、列表、浏览、用户登录、搜索等功能。

博客网站（暂无域名）： http://218.78.54.114:5000/

博客首页示例:
<img src="https://github.com/fenife/yonder_old/blob/master/yonder-home-example.jpg" alt="博客示例" title="博客示例">

文章详情示例:
<img src="https://github.com/fenife/yonder_old/blob/master/yonder-detail-example.jpg" alt="文章详情示例" title="文章详情示例">

## 本地开发
1. 进入项目目录后，新增本地开发配置文件：
```bash
cp dev/example.env dev/.env
```
2. 填写`dev/.env`对应的配置项目
3. 进入`dev`目录执行以下的命令启动服务：
```bash
cd dev

# 运行mysql、redis、前端服务
make dev

# 进入后端容器
make as

# 手动启动后端服务
# 因为需要在 docker compose 中通过 watchdog 监控文件变化并自动重启服务，方便开发
# 但是这里的 docker compose 对文件的监控还有问题，暂时先手动启动服务
./start-dev.sh
```

4. 服务停止：
```bash
make down
```


## 部署
本服务包含了前端渲染服务、后端接口服务、mysql、redis等多个应用服务，如果直接部署在云服务器上，可能需要比较多的配置，管理起来也比较复杂； 所以这里通过 docker compose 进行容器化部署，对服务器的硬件资源要求会更高一点，但是便于环境隔离、易于迁移，方便后续的管理维护。

1. 进入项目目录后，新增配置文件：
```bash
# docker compose 中 mysql 等服务的配置文件
cp dockerbuild/example.env dockerbuild/.env

# 后端服务配置文件
cp server_py/config/yonder-example.json server_py/config/yonder.json
```

2. 填写`dockerbuild/.env`和`server_py/config/yonder.json`对应的配置项目

3. 执行以下的命令启动服务：
```bash
# 前台运行
make up

# 后台运行
make upd
```

4. 服务停止：
```bash
make down
```

> 命令参考：`Makefile`文件

## 技术栈
- 后端
    - 语言：Python、Golang
    - 框架：自实现web框架sim、gin
    - 组件：MySQL、Redis
- 前端
    - 语言：javascript
    - 框架：vue、nuxt

## 部分缩写
- sim: simple micro framework
- ydr: yonder
- wes: web service
- aps: app service
- ses: search service

## DONE
- 业务侧：
    - 用户登陆、管理员角色和权限
    - 文章创建、更新、删除（需管理员权限）
    - 文章列表、分页
    - 文章详情、上一篇、下一篇
    - 标签创建、更新、删除（需管理员权限）
    - 标签列表和文章数目统计
    - 按标题搜索文章
    - 归档页：
        - 文章按时间线显示
        - 统计每年的文章数

- 技术侧：
    - 自实现的Web框架sim (Python)
    - 自实现的ORM框架norm (Python)
    - 通过 docker 构建、docker compose 部署
    - 通过docker和compose搭建本地开发环境，可自动监控本地变化的文件并重启服务

## TODO
- 业务侧：
    - 顶栏固定，不随文章详情滚动
    - 支持图片浏览、图床保存图片
    - 支持 plantuml 画图
    - 浏览次数统计
    - 支持全文搜索
    - 注册
    - 评论
    - 支持合辑
    - 首页文章列表，作者、时间、标签的UI优化
    - 最近更新
    - 归档：
        - 按月份+统计
    - 分类：
        - 按总数排行，显示前10条
        - 超过后显示更多按钮

- 技术侧：
    - 创建默认管理员，单独用一个脚本，跟main.py分开
    - 不显示id，用md5
    - 文章列表按created_at排序，方便后续数据导入和恢复
    - 线程池

    - 修复启动错误：
        - mkdir: cannot create directory ‘/var/yonder’: Permission denied
        - '\r': command not found

    - docker compose 中通过 python watchdog 监控文件变化，自动重启服务，方便开发

    - docker ignore


