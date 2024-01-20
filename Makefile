
# docker run -it python:3.7 bash
# docker run -it ubuntu:20.10 bash

ubuntu-base = ubuntu-base
frontend-image = yonder-frontend
server-py3 = server-py3

bu:
	docker build -f dockerbuild/dockerfile.ubuntu -t $(ubuntu-base) .

eu:
	docker run --rm -it $(ubuntu-base) bash 


bf:
	docker build -f dockerbuild/dockerfile.frontend -t $(frontend-image) .

rf:
	docker run --name $(frontend-image) --rm -it $(frontend-image) 

ef:
	docker run --rm -it $(frontend-image) bash


bs:
	docker build -f dockerbuild/dockerfile.server.py3 -t $(server-py3) .

rs:
	docker run --name $(server-py3) --rm -it -p 6070:6070 $(server-py3) 

es:
	docker run --rm -it $(server-py3) /bin/bash



