
.PHONY: run stop as 

run: 
	docker build -f ../dockerbuild/dockerfile.ubuntu -t ubuntu-base ..
	docker build -f dockerfile.frontend -t yonder-frontend:dev ..
	docker build -f dockerfile.server.py -t yonder-server-py:dev ..
	docker build -f dockerfile.server.go -t yonder-server-go:dev ..
	docker compose -f docker-compose.yml up	

stop:
	docker compose -f docker-compose.yml down

py:
	docker exec -it yonder-server-py-dev /bin/bash

js:
	docker exec -it yonder-frontend-dev /bin/bash

go:
	docker exec -it yonder-server-go-dev /bin/bash

dev-py:
	docker run --rm -it -v .:/yonder yonder-server-py:dev /yonder/server_py/start-dev.sh

build-go:
	docker build -f dockerfile.server.go -t yonder-server-go:dev ..