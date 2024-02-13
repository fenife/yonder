package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"server-go/config"
	"server-go/controller/middleware"
	"server-go/router"

	_ "server-go/docs" // 导入swag生成的接口文档
)

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

	router.AddRouter(engine)

	if err := engine.Run(config.Conf.Server.ServerAddr()); err != nil {
		panic(fmt.Sprintf("run app failed: %v", err))
	}
}
