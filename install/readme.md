# install
install.md  安装说明
fabfile.py  fabric远程部署python脚本
install.sh  旧的部署shell脚本，现在已经用不到了，也不会再更新，
            里面的内容仅用作参考
            
## usage
1. 进入本目录（必须）
2. 修改`fabfile.py`，把`_deploy_env`设置为要部署的环境`test`或`live`
3. 执行`fab -l`看有哪些部署的选项

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
restore backup data to remote mysql
