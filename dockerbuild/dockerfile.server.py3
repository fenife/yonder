FROM ubuntu-base

ARG HOME_DIR=/yonder
ARG SERVER_PY3_DIR=/yonder/server_py3

RUN mkdir -p ${SERVER_PY3_DIR}
WORKDIR ${SERVER_PY3_DIR}

COPY src/server_py3/requirements.txt ${SERVER_PY3_DIR}/
RUN pip3 install -r requirements.txt

COPY etc/server/yonder.json ${SERVER_PY3_DIR}/

COPY src/server_py3 .

EXPOSE 6070

CMD [ "bash", "docker-entrypoint.sh"]


