
## 文件说明
xxx_dev.py      开发环境配置（一般也是本地环境，不需要远程部署）
xxx_test.py     测试环境配置（可远程部署）
xxx_live.py     正式环境配置（远程部署）

## 配置使用说明
此目录下的`*.py`文件同时也是配置文件，但是除了python外，其他语言无法读取

修改里面的配置后，还要转换为json文件，并重命名，方便其他服务读取配置内容

比如：
原始的配置文件为： yonder_dev.py

修改里面的配置内容后，需要转换： python3 yonder_dev.py
执行后，会生成同名的json文件： yonder_dev.json

重命名： mv yonder_dev.json yonder.json

## Makefile
该目录提供了Makefile文件，方便转换操作

make dev        生成dev环境json配置文件
make test
make live
make clean      清除所有json配置文件

