package utils

import (
	"fmt"
	"github.com/go-redis/redis/v7"
	"log"
	yconf "yonder/config"
)

func NewRedisClient() *redis.Client {
	yc := yconf.Conf

	addr := fmt.Sprintf("%s:%d", yc.RedisHost, yc.RedisPort)
	client := redis.NewClient(&redis.Options{
		Addr:     addr,
		DB:       0,  // use default DB
	})

	_, err := client.Ping().Result()
	if err != nil {
		log.Println("can not connect to redis")
		return nil
	}
	return client
}
