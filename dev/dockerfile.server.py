FROM ubuntu-base

# 先安装依赖
COPY server_py/requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /yonder/server_py

# CMD [ "/bin/bash", "-c", "while true;do sleep 600;done"]
