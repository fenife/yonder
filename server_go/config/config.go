package config

import (
	"encoding/json"
	"fmt"
	"os"
)

type ServerConfig struct {
	Host string `json:"host"`
	Port int    `json:"port"`
}

func (s *ServerConfig) ServerAddr() string {
	return fmt.Sprintf("%s:%d", s.Host, s.Port)
}

type MysqlConfig struct {
	Host     string `json:"host"`
	Port     int    `json:"port"`
	User     string `json:"user"`
	Password string `json:"password"`
	Database string `json:"database"`
	Charset  string `json:"charset"`
}

type RedisConfig struct {
	Host string `json:"host"`
	Port int    `json:"port"`
}

type Config struct {
	Env    string       `json:"env"`
	Server ServerConfig `json:"server"`
	Mysql  MysqlConfig  `json:"mysql"`
	Redis  RedisConfig  `json:"redis"`
}

var Conf Config

func init() {
	// 相对 main.go 执行文件的路径
	configFile := "./config/server.json"
	data, err := os.ReadFile(configFile)
	if err != nil {
		panic(fmt.Sprintf("read config file failed: %v", err))
	}
	if err := json.Unmarshal(data, &Conf); err != nil {
		panic(fmt.Sprintf("unmarshal config data failed: %v", err))
	}
}
