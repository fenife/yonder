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

	swaggerFiles "github.com/swaggo/files"     // swagger embed files
	ginSwagger "github.com/swaggo/gin-swagger" // gin-swagger middleware
	_ "server-go/docs"                         // 导入swag生成的接口文档
)

func addRouter(engine *gin.Engine) {
	engine.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})

	// swag文档
	engine.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	repos, err := persistence.NewRepos(&config.Conf.Mysql)
	if err != nil {
		panic(err)
	}
	userApp := application.NewUserApp(repos.UserRepo)
	userHandler := handler.NewUserHandler(userApp)

	engine.POST("/user", userHandler.CreateUser)
}

// @title yonder blog api
// @version 1.0
// @description yonder博客的后端API服务
// @termsOfService http://swagger.io/terms/

// @host localhost:8030
// @BasePath /
func main() {
	engine := gin.New()
	//gin.SetMode(gin.ReleaseMode)

	engine.Use(
		middleware.RequestIdMiddleware(),
		middleware.LogContext(),
		gin.Recovery(),
	)

	addRouter(engine)

	if err := engine.Run(config.Conf.Server.ServerAddr()); err != nil {
		panic(fmt.Sprintf("run app failed: %v", err))
	}
}
