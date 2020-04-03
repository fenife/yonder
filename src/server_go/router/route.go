package router

import (
	"github.com/gin-gonic/gin"
	yapi "yonder/api"
)

func Route(router *gin.Engine) {
	apiGrp := router.Group("/api")

	// 搜索
	apiGrp.GET("/search", yapi.SearchArticle)
	apiGrp.GET("/", yapi.Hello)
}
