package persistence

import (
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
	"server-go/config"
	"server-go/domain/repo"
)

type Repos struct {
	UserRepo repo.IUserRepo
	db       *gorm.DB
}

func NewRepos(mysqlConf *config.MysqlConfig) (*Repos, error) {
	db, err := gorm.Open(mysql.Open(mysqlConf.ConnStr()), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Info),
	})
	if err != nil {
		return nil, err
	}
	//db.LogMode(true)

	return &Repos{
		UserRepo: NewUserRepo(db),
		db:       db,
	}, nil
}
