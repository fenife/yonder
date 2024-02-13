package entity

import "server-go/pkg/utils"

type User struct {
	BaseModel

	Name         string `gorm:"type:varchar(256);not null;unique;comment:'用户名'" json:"name"`
	PasswordHash string `gorm:"type:varchar(100);not null;comment:'密码'" json:"password_hash"`
	//Status       int8   `gorm:"type:tinyint;not null;comment:'用户状态'" json:"status"`
}

func (u *User) VerifyPassword(password string) bool {
	// 这里的password还是明文密码
	return utils.Md5(password) == u.PasswordHash
}
