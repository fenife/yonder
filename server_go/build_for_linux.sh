#!/usr/bin/env bash

cur=`pwd`

# export GOPATH=$GOPATH:${cur}
export GOPATH=~/go:${cur}

CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o yonder_server_go main.go
