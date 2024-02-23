
.PHONY: run rund stop

ubuntu-base = ubuntu-base
yonder-frontend = yonder-frontend
yonder-server-py = yonder-server-py
yonder-server-go = yonder-server-go

# ubuntu base

bu:
	docker build -f dockerbuild/dockerfile.ubuntu -t $(ubuntu-base) .

eu: bu
	docker run --rm -it $(ubuntu-base) bash 

# frontend

bf:
	docker build -f dockerbuild/dockerfile.frontend -t $(yonder-frontend) .

rf: bf
	docker run --name $(yonder-frontend) --rm -it -p 6050:6050 $(yonder-frontend) 

ef: bf
	docker run --rm -it $(yonder-frontend) bash

# server_py

build-py: 
	docker build -f dockerbuild/dockerfile.server.py -t $(yonder-server-py) .

run-py: build-py
	docker run --name $(yonder-server-py) --rm -it -p 8010:8010 $(yonder-server-py) 

enter-py: build-py
	docker run --rm -it $(yonder-server-py) bash

py: 
	docker exec -it $(yonder-server-py) bash

# server_go
build-go: 
	docker build -f dockerbuild/dockerfile.server.go -t $(yonder-server-go) .

run-go: build-go
	docker run --name $(yonder-server-go) --rm -it -p 8020:8020 $(yonder-server-go) 

enter-go: build-go
	docker run --rm -it $(yonder-server-go) bash

go: 
	docker exec -it $(yonder-server-go) bash

# bash 脚本文件换行符格式化
format:
	find . -name "*.sh" | xargs dos2unix

# all
run: format bu bf build-py 
	docker compose -f dockerbuild/docker-compose.yml up

rund: format bu bf build-py
	find . -name "*.sh" | xargs dos2unix
	docker compose -f dockerbuild/docker-compose.yml up -d

stop:
	docker compose -f dockerbuild/docker-compose.yml down

