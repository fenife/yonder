FROM ubuntu-base

WORKDIR /yonder/server_go

# 先安装依赖
COPY server_go/go.* ./
RUN go mod download

# CMD [ "/bin/bash", "-c", "while true;do sleep 600;done"]
