package main

// read config
// logger
// gorm

import (
	"io"
	"log"
	"os"
	yconf "yonder/config"
	"yonder/router"

	"github.com/gin-gonic/gin"
)

func logInit() {
	// todo: TimedRotatingFileHandler
	logPath := yconf.Conf.LogPath + "/server_go"
	logFile := logPath + "/srv.log" // todo: rename
	if err := os.MkdirAll(logPath, os.ModePerm); err != nil {
		panic(err)
	}

	//fp, err := os.Create(logFile)
	fp, err := os.OpenFile(logFile, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		panic(err)
	}
	// gin logger
	w := io.MultiWriter(fp, os.Stdout)
	gin.DefaultWriter = w

	// std logger
	log.SetOutput(gin.DefaultWriter)
	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)
}

func main() {
	logInit()

	// Creates a router without any middleware by default
	app := gin.New()

	// Global middleware
	// Logger middleware will write the logs to gin.DefaultWriter even if you set with GIN_MODE=release.
	// By default gin.DefaultWriter = os.Stdout
	app.Use(gin.Logger())

	// Recovery middleware recovers from any panics and writes a 500 if there was one.
	app.Use(gin.Recovery())

	router.Route(app)

	err := app.Run(":6060")
	if err != nil {
		panic(err.Error())
	}
}
