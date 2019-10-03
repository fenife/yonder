#!/usr/bin/env bash

cur=`pwd`

# export GOPATH=$GOPATH:${cur}
export GOPATH=~/go:${cur}

echo $GOPATH

# go run main_test.go
go test -count=1 main_test.go 
