package entity

import (
	"github.com/google/uuid"
	"server-go/domain/do"
	"server-go/pkg/utils"
	"strconv"
	"time"
)

type User struct {
	BaseModel

	Name         string `gorm:"type:varchar(255);not null;unique;comment:'用户名'" json:"name"`
	PasswordHash string `gorm:"type:varchar(100);not null;comment:'密码'" json:"password_hash"`
	//Status       int8   `gorm:"type:tinyint;not null;comment:'用户状态'" json:"status"`
}

func (u *User) GenPasswordHash(password string) string {
	//return utils.Md5(fmt.Sprintf("%s-%s", config.Conf.Server.SecretKey, password))
	return utils.Md5(password)
}

func (u *User) VerifyPassword(password string) bool {
	// 这里的password还是明文密码
	return u.GenPasswordHash(password) == u.PasswordHash
}

func (u *User) GenUserToken() string {
	// 随机字符串
	return utils.Md5(uuid.New().String() + strconv.Itoa(time.Now().Second()))
}

// 检查用户是否正常
func (u *User) IsValid() bool {
	// 未删除，且uid>0
	return u.DeletedAt.Valid == false && u.ID > 0
}

func (u *User) ToTiny() *do.UserTiny {
	if u == nil {
		return nil
	}
	newUser := do.UserTiny{
		ID:   u.ID,
		Name: u.Name,
	}
	return &newUser
}

func (u *User) ToSmall() *do.UserSmall {
	if u == nil {
		return nil
	}
	newUser := do.UserSmall{
		ID:        u.ID,
		CreatedAt: u.CreatedAt.Format(timeFormatLayout),
		UpdatedAt: u.CreatedAt.Format(timeFormatLayout),
		Name:      u.Name,
	}
	return &newUser
}
