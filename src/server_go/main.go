package main

// read config
// logger

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/go-redis/redis/v7"
	yconf "yonder/config"
	yutil "yonder/utils"
)

// redis client
var rds = redis.NewClient(&redis.Options{
	Addr: "localhost:6379",
})

func hello(c *gin.Context) {
	v, _ := rds.Get("hello").Result()
	c.JSON(200, gin.H{
		"value": v,
		"msg":   "hello world",
	})
}

func main() {
	// 创建一个默认的路由引擎
	r := gin.Default()

	// GET /hello 时，会执行hello函数
	r.GET("/hello", hello)

	v, err := rds.Set("hello", "world", 0).Result()
	fmt.Println(v, err)

	// 启动HTTP服务，默认在0.0.0.0:6060启动服务
	r.Run(":6060")
	//fmt.Println()
	yutil.PrettyPrint(yconf.Conf)
	//ReadConf()
}
