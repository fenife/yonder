# yonder
搭建一个博客网站，实现了文章发布、标签分类、列表、浏览、用户登录、搜索等功能。

博客网站（暂无域名）： http://218.78.54.114:6050

博客首页示例:
<img src="https://github.com/fenife/yonder_old/blob/master/yonder-home-example.jpg" alt="博客示例" title="博客示例">

文章详情示例:
<img src="https://github.com/fenife/yonder_old/blob/master/yonder-detail-example.jpg" alt="文章详情示例" title="文章详情示例">

## 技术栈
    后端：
        golang
        Python
        mysql
        redis
        nginx
    
    前端：
        javascript
        vue 
        nuxt
        
## 部署
执行以下的命令启动服务：
```bash
# 前台运行
make up

# 后台运行
make upd
```

服务停止：
```bash
make down
```

命令参考：`Makefile`

## 部分缩写
    sim: simple micro framework
    ydr: yonder
    wes: web service
    aps: app service
    ses: search service

## TODO
- 不显示id，用md5
- 顶栏固定，不随文章详情滚动
- 支持图片浏览
- 支持 plantuml 画图
- 浏览次数统计
- 支持全文搜索
- 注册
- 评论
