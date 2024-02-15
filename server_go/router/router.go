package router

import (
	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
	service2 "server-go/application/service"
	"server-go/config"
	"server-go/controller/handler"
	mw "server-go/controller/middleware"
	"server-go/domain/service"
	"server-go/infra/cache/redisc"
	"server-go/infra/persistence"
)

func AddRouter(engine *gin.Engine) {
	// swag文档
	engine.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	// 资源初始化
	repos, err := persistence.NewRepos(&config.Conf.Mysql)
	if err != nil {
		panic(err)
	}
	caches, err := redisc.NewCaches(&config.Conf.Redis)
	if err != nil {
		panic(err)
	}
	domainServices := service.NewDomainServices(repos.UserRepo, caches.UserCache)
	apps := service2.NewApps(domainServices.UserDomain)
	hdr := handler.NewHandlers(apps.UserApp)

	// 添加路由
	engine.GET("/ping", hdr.PingHandler.Ping)
	apiV1 := engine.Group("/api/v1")
	{
		user := apiV1.Group("user")
		{
			user.POST("/signup", hdr.UserHandler.UserSignup)
			user.POST("/signin", hdr.UserHandler.UserSignIn)
			user.POST("/signout", mw.UserAuthMiddleware(caches.UserCache), hdr.UserHandler.UserSignOut)
		}
	}
}
