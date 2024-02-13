package router

import (
	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
	"server-go/application"
	"server-go/config"
	"server-go/controller/handler"
	"server-go/infra/persistence"
)

type ControllerHandler struct {
	pingHandler *handler.PingHandler
	userHandler *handler.UserHandler
}

func NewControllerHandler() *ControllerHandler {
	repos, err := persistence.NewRepos(&config.Conf.Mysql)
	if err != nil {
		panic(err)
	}
	userApp := application.NewUserApp(repos.UserRepo)

	return &ControllerHandler{
		pingHandler: handler.NewPingHandler(),
		userHandler: handler.NewUserHandler(userApp),
	}
}

func AddRouter(engine *gin.Engine) {
	// swag文档
	engine.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	hdr := NewControllerHandler()

	engine.GET("/ping", hdr.pingHandler.Ping)

	apiV1 := engine.Group("/api/v1")
	{
		user := apiV1.Group("user")
		{
			user.POST("/signup", hdr.userHandler.UserSignup)
		}
	}
}
