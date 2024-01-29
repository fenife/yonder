
.PHONY: dev

dev: 
	docker build -f ../dockerbuild/dockerfile.ubuntu -t ubuntu-base ..
	docker build -f dockerfile.frontend -t yonder-frontend:dev ..
	docker build -f dockerfile.server.py3 -t yonder-server-py3:dev ..
	docker compose -f docker-compose.yml up	

stop:
	docker compose -f docker-compose.yml down

as:
	docker exec -it yonder-server-dev /bin/bash

dev-es:
	docker run --rm -it -v ./src/server_py3:/yonder/server_py3 server-py3:dev1 /yonder/server_py3/start-dev.sh
