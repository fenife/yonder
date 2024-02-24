FROM ubuntu-base

# 先安装依赖
COPY server_py/requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ARG YONDER_HOME=/yonder
ARG SERVER_DIR=/yonder/server_py

RUN mkdir -p ${SERVER_DIR}
WORKDIR ${SERVER_DIR}

COPY pylib ${YONDER_HOME}/pylib
COPY server_py .

EXPOSE 6070

CMD [ "bash", "docker-entrypoint.sh"]


