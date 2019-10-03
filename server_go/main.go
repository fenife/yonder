// blog server main

package main

import (
	"fmt"
	"io"
	"log"
	"os"

	"github.com/gin-gonic/gin"

	"backend/config"
	"backend/model"
	"backend/router"
)

func migrate() {
	var dc = config.AllConfig.Database
	db := model.DB

	options := fmt.Sprintf("ENGINE=InnoDB CHARSET=%s auto_increment=1;", dc.Charset)

	db.Set("gorm:table_options", options).AutoMigrate(&model.Category{})
	db.Set("gorm:table_options", options).AutoMigrate(&model.Article{})
	db.Set("gorm:table_options", options).AutoMigrate(&model.User{})

	//db.AutoMigrate(&model.User{})
	//db.AutoMigrate(&model.Category{})
	//db.AutoMigrate(&model.Article{})

	model.CreateAdminUser()
}

func logInit() {
	var logPath = config.AllConfig.Server.LogPath
	logFile, err := os.Create(logPath)
	if err != nil {
		panic(err)
	}
	// gin logger
	w := io.MultiWriter(logFile, os.Stdout)
	gin.DefaultWriter = w

	// std logger
	log.SetOutput(gin.DefaultWriter)
	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)

	// new logger
	//logFlags := log.Ldate | log.Ltime | log.Lshortfile
	//logger := log.New(w, "\r\n", 0)
	//logger.Println("test")
}

func main() {
	logInit()

	log.Println(fmt.Sprintf("env mode: %s", config.AllConfig.Server.Mode))

	if config.IsRelease() {
		gin.SetMode(gin.ReleaseMode)
	}

	// create table
	migrate()

	// Creates a router without any middleware by default
	app := gin.New()

	// Global middleware
	// Logger middleware will write the logs to gin.DefaultWriter even if you set with GIN_MODE=release.
	// By default gin.DefaultWriter = os.Stdout
	app.Use(gin.Logger())

	// Recovery middleware recovers from any panics and writes a 500 if there was one.
	app.Use(gin.Recovery())

	router.Route(app)

	app.Run(":6060")
}
