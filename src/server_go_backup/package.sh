#!/usr/bin/env bash

set -x

GOPATH=~/go
mkdir -p $GOPATH/src/golang.org/x/
cd $GOPATH/src/golang.org/x/
git clone https://github.com/golang/net.git net
go install net

go get github.com/gin-gonic/gin
go get github.com/garyburd/redigo/redis
go get github.com/jinzhu/gorm
go get github.com/go-sql-driver/mysql
go get github.com/microcosm-cc/bluemonday
go get github.com/russross/blackfriday
