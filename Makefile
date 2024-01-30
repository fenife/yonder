
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
	docker exec -it yonder-server /bin/bash

up: bu bf bs
	bash start.sh
	docker compose -f dockerbuild/docker-compose.yml up

upd:
	bash start.sh
	docker compose -f dockerbuild/docker-compose.yml up -d

down:
	docker compose -f dockerbuild/docker-compose.yml down
	