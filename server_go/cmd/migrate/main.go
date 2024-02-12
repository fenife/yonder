package main

import (
	"fmt"
	"github.com/go-gormigrate/gormigrate/v2"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
	"log"
	"server-go/config"
)

var migrations = make([]*gormigrate.Migration, 0)

func main() {
	db, err := gorm.Open(mysql.Open(config.Conf.Mysql.ConnStr()), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Info),
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(migrations)

	m := gormigrate.New(db, gormigrate.DefaultOptions, migrations)
	if err = m.Migrate(); err != nil {
		log.Fatalf("Migration failed: %v", err)
	}
	log.Println("Migration run successfully")
}
