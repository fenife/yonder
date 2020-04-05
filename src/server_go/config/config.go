package config

import (
	"encoding/json"
	"io/ioutil"
)

type serverConfig struct {
	EnvMode     string   `json:"ENV_MODE"`
	SshHosts    []string `json:"SSH_HOSTS"`
	SshUser     string   `json:"SSH_USER"`
	SshSudoUser string   `json:"SSH_SUDO_USER"`
	DebugMode   int      `json:"DEBUG_MODE"`

	DBHost     string `json:"DB_HOST"`
	DBPort     int    `json:"DB_PORT"`
	DBUser     string `json:"DB_USER"`
	DBPassword string `json:"DB_PASSWORD"`
	DBName     string `json:"DB_NAME"`
	DBCharset  string `json:"DB_CHARSET"`

	RedisHost string `json:"REDIS_HOST"`
	RedisPort int    `json:"REDIS_PORT"`

	SecretKey     string `json:"SECRET_KEY"`
	AdminUsername string `json:"ADMIN_USERNAME"`
	AdminPassword string `json:"ADMIN_PASSWORD"`
	PageSize      int    `json:"PAGE_SIZE"`
	LoginExpired  int    `json:"LOGIN_EXPIRED"`

	LogFile string `json:"LOG_FILE"`
	LogPath string `json:"LOG_PATH"`

	BackupDBHost     string `json:"BACKUP_DB_HOST"`
	BackupDBPort     int    `json:"BACKUP_DB_PORT"`
	BackupDBUser     string `json:"BACKUP_DB_USER"`
	BackupDBPassword string `json:"BACKUP_DB_PASSWORD"`
	BackupDBName     string `json:"BACKUP_DB_NAME"`
	BackupDBCharset  string `json:"BACKUP_DB_CHARSET"`
}

const confFile = "/icode/yonder/etc/server/yonder.json"

var Conf serverConfig

//func ReadConf() map[string]interface{} {
func loadConf() {
	data, err := ioutil.ReadFile(confFile)
	if err != nil {
		panic(err.Error())
	}

	if err := json.Unmarshal(data, &Conf); err != nil {
		panic(err.Error())
	}
}

func IsDev() bool {
	return Conf.EnvMode == "dev"
}

func IsDebugMode() bool {
	return Conf.DebugMode == 1
}

func init() {
	loadConf()
}
