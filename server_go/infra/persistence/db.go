package persistence

import (
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
	"server-go/config"
	"server-go/domain/repo"
)

type Repos struct {
	db       *gorm.DB
	UserRepo repo.IUserRepo
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
		db:       db,
		UserRepo: NewUserRepo(db),
	}, nil
}
