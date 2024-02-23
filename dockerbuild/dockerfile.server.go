FROM ubuntu-base

WORKDIR /yonder/server_go

# 先安装依赖
COPY server_go/go.* ./
RUN go mod download

ARG YONDER_HOME=/yonder
ARG SERVER_DIR=/yonder/server_go

RUN mkdir -p ${SERVER_DIR}
WORKDIR ${SERVER_DIR}

COPY server_go .

RUN CGO_ENABLED=0 GOOS=linux go build  -o migrate ./cmd/migrate
RUN CGO_ENABLED=0 GOOS=linux go build -o ./server_go


EXPOSE 8020

CMD [ "bash", "docker-entrypoint.sh"]
