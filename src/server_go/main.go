package main

import (
	"github.com/gin-gonic/gin"
)

func hello(c *gin.Context) {
	c.JSON(200, gin.H{
		"msg": "hello world",
	})
}

func main() {
	// 创建一个默认的路由引擎
	r := gin.Default()

	// GET /hello 时，会执行hello函数
	r.GET("/hello", hello)

	// 启动HTTP服务，默认在0.0.0.0:8080启动服务
	r.Run(":6060")
}