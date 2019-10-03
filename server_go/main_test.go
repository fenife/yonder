package main

import (
	"backend/debug"
	"backend/model"
	"github.com/garyburd/redigo/redis"
	"testing"
)

func TestUser(t *testing.T) {
	db := model.DB

	db.AutoMigrate(&model.User{})
	db.AutoMigrate(&model.Category{})

	// 创建
	db.Create(&model.User{
		Name:   "jack",
		Role:   model.UserRoleNormal,
		Status: model.UserStatusActive,
	})

	// 读取
	var user model.User
	db.First(&user, 1)
	db.First(&user, "name = ?", "jack")
	if user.Name != "jack" {
		t.Errorf(`[Create] user name ="%s"; want "jack"`, user.Name)
	}

	// 更新
	db.Model(&user).Update("Name", "bingo")

	// 删除
	//db.Delete(&user)
}

func TestRedis(t *testing.T) {
	rds := model.RedisPool.Get()
	defer rds.Close()

	if _, err := rds.Do("SET", "hello", "world"); err != nil {
		dbg.Dbg(err)
	}

	got, err := redis.String(rds.Do("GET", "hello"))
	if err != nil {
		t.Errorf(`[GET] hello="%s"; err: %s`, got, err)
	}
	if got != "world" {
		t.Errorf(`[GET] hello="%s"; want "world"`, got)
	}
}
