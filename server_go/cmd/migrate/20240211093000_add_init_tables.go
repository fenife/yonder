package main

import (
	"github.com/go-gormigrate/gormigrate/v2"
	"gorm.io/gorm"
	"server-go/domain/entity"
)

func init() {
	migrations = append(migrations, &gormigrate.Migration{
		ID: "20240211093000",
		Migrate: func(tx *gorm.DB) error {
			type user struct {
				entity.User
			}
			return tx.Migrator().CreateTable(&user{})
		},
		Rollback: func(tx *gorm.DB) error {
			return tx.Migrator().DropTable("users")
		},
	})
}
