
# docker run -it python:3.7 bash
# docker run -it ubuntu:20.10 bash

ubuntu-base = ubuntu-base
frontend-image = yonder-frontend
server-py3 = server-py3

# ubuntu base

bu:
	docker build -f dockerbuild/dockerfile.ubuntu -t $(ubuntu-base) .

eu:
	docker run --rm -it $(ubuntu-base) bash 

# frontend

bf:
	docker build -f dockerbuild/dockerfile.frontend -t $(frontend-image) .

rf:
	docker run --name $(frontend-image) --rm -it -p 6050:6050 $(frontend-image) 

ef:
	docker run --rm -it $(frontend-image) bash

# server

bs:
	docker build -f dockerbuild/dockerfile.server.py3 -t $(server-py3) .

rs:
	docker run --name $(server-py3) --rm -it -p 6070:6070 $(server-py3) 

es:
	docker run --rm -it $(server-py3) /bin/bash

as: 
	docker exec -it yonder-backend /bin/bash


up: bu bf bs
	docker compose -f dockerbuild/docker-compose.yml up
