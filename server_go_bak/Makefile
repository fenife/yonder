
.PHONY: build-linux build-macos run clean

build-linux:
	CGO_ENABLED="0" GOOS="linux" GOARCH="amd64" go build -o yonder_server_go main.go

build-macos:
	CGO_ENABLED="0" GOOS="darwin" GOARCH="amd64" go build -o yonder_server_go main.go

run:
	go run main.go

clean:
	rm ./yonder_server_go