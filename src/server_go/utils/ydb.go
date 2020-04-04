package utils

import (
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"github.com/jinzhu/gorm"
	"time"
	yconf "yonder/config"
)

var DB *gorm.DB

func initDB() {
	//var dc = config.AllConfig.Database
	yc := yconf.Conf
	mysqlUrl := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=%s&parseTime=true&loc=Local",
		yc.DBUser, yc.DBPassword, yc.DBHost, yc.DBPort, yc.DBName, yc.DBCharset)

	db, err := gorm.Open("mysql", mysqlUrl)
	if err != nil {
		fmt.Println("mysql config: ", mysqlUrl)
		panic(err.Error())
	}
	db.DB().SetConnMaxLifetime(time.Minute * 5)
	db.DB().SetMaxIdleConns(0)
	db.DB().SetMaxOpenConns(10)

	// log sql generated by gorm
	if yconf.IsDev() {
		db.LogMode(true)
	}

	DB = db
}

func init() {
	initDB()
}