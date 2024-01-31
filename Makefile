
ubuntu-base = ubuntu-base
yonder-frontend = yonder-frontend
yonder-server-py = yonder-server-py

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

# server

bs: bs
	docker build -f dockerbuild/dockerfile.server.py -t $(yonder-server-py) .

rs: bs
	docker run --name $(yonder-server-py) --rm -it -p 6070:6070 $(yonder-server-py) 

es: bs
	docker run --rm -it $(yonder-server-py) /bin/bash

as: 
	docker exec -it $(yonder-server-py) /bin/bash

# all
up: bu bf bs
	bash start.sh
	docker compose -f dockerbuild/docker-compose.yml up

upd: bu bf bs
	bash start.sh
	docker compose -f dockerbuild/docker-compose.yml up -d

down:
	docker compose -f dockerbuild/docker-compose.yml down
