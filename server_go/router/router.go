package router

import (
	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
	"server-go/application"
	"server-go/config"
	"server-go/controller/handler"
	"server-go/domain/service"
	"server-go/infra/cache/redisc"
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

	caches, err := redisc.NewCaches(&config.Conf.Redis)
	if err != nil {
		panic(err)
	}

	userDomainService := service.NewUserDomainService(repos.UserRepo, caches.UserCache)
	userApp := application.NewUserApp(userDomainService)

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
			user.POST("/signin", hdr.userHandler.UserSignIn)
		}
	}
}
