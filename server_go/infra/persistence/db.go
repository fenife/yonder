package persistence

import (
	"gorm.io/gorm"
	"server-go/config"
	"server-go/domain/repo"
	"server-go/pkg/gormx"
)

type Repos struct {
	db       *gorm.DB
	UserRepo repo.IUserRepo
}

func NewRepos(mysqlConf *config.MysqlConfig) (*Repos, error) {
	db, err := gormx.NewGormMysqlDB(mysqlConf)
	if err != nil {
		return nil, err
	}
	//db.LogMode(true)

	return &Repos{
		db:       db,
		UserRepo: NewUserRepo(db),
	}, nil
}
