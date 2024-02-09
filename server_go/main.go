package main

import (
	"fmt"
	"github.com/fenife/yonder/server_go/config"
	"github.com/gin-gonic/gin"
	"net/http"
)

func main() {
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})

	if err := r.Run(config.Conf.Server.ServerAddr()); err != nil {
		panic(fmt.Sprintf("run app failed: %v", err))
	}
}
