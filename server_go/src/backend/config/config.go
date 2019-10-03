package config

import (
	"encoding/json"
	"io/ioutil"
	"regexp"

	_ "github.com/go-sql-driver/mysql"

	"backend/debug"
)

type DbConfig struct {
	Host 		string
	Port 		int
	User		string
	Password	string
	DbName 		string
	Charset		string
}

type RedisConfig struct {
	Host 		string
	Port 		int
	MaxIdle		int
	MaxActive	int
}

type ServerConfig struct {
	Mode 	string
	Salt	string
	LogPath string
}

type AdminConfig struct {
	Name 		string
	Password 	string
}

type PageConfig struct {
	Size 	int
}

type allConfig struct {
	Database 	DbConfig		`json:"database"`
	Redis		RedisConfig		`json:"redis"`
	Server 		ServerConfig 	`json:"server"`
	Admin 		AdminConfig 	`json:"admin"`
	Page 		PageConfig		`json:"page"`
}

// 加载json配置
//var jsonData map[string]interface{}
var AllConfig allConfig

func loadConf(cfgFile string) {
	data, err := ioutil.ReadFile(cfgFile)
	if err != nil {
		panic(err.Error())
	}

	// 去掉json中的注释
	confStr := string(data)
	reg := regexp.MustCompile(`/\*.*\*/`)
	confStr = reg.ReplaceAllString(confStr, "")
	data = []byte(confStr)

	if err := json.Unmarshal(data, &AllConfig); err != nil {
		panic(err.Error())
	}
	dbg.Dbg("AllConfig:", AllConfig)
}

func IsDev() bool {
	return AllConfig.Server.Mode == "dev"
}

func IsRelease() bool {
	return AllConfig.Server.Mode == "release"
}

func InitConf()  {
	confFile := "config.json"
	loadConf(confFile)
}

func init() {
	InitConf()
}
