FROM ubuntu-base

ARG SERVER_PY3_DIR=/yonder/server_py3

WORKDIR ${SERVER_PY3_DIR}

COPY src/server_py3/requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# CMD [ "/bin/bash", "-c", "while true;do sleep 1;done"]
