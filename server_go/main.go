package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"server-go/application"
	"server-go/config"
	"server-go/controller/handler"
	"server-go/controller/middleware"
	"server-go/infra/persistence"
)

func addRouter(engine *gin.Engine) {
	engine.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})

	repos, err := persistence.NewRepos(&config.Conf.Mysql)
	if err != nil {
		panic(err)
	}
	userApp := application.NewUserApp(repos.UserRepo)
	userHandler := handler.NewUserHandler(userApp)

	engine.POST("/user", userHandler.CreateUser)
}

func main() {
	engine := gin.Default()

	engine.Use(
		//middleware.RequestIdMiddleware(),
		middleware.LogContext(),
	)

	addRouter(engine)

	if err := engine.Run(config.Conf.Server.ServerAddr()); err != nil {
		panic(fmt.Sprintf("run app failed: %v", err))
	}
}
