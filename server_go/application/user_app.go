package application

import (
	"context"
	"html"
	"server-go/domain/entity"
	"server-go/domain/service"
)

type IUserApp interface {
	Signup(ctx context.Context, username, passwd string) (*entity.User, error)
	SignIn(ctx context.Context, username, passwd string) (*entity.User, string, error)
	GetUserList(ctx context.Context) ([]entity.User, error)
}

type UserApp struct {
	userDomain service.IUserDomain
}

func NewUserApp(userDomain service.IUserDomain) *UserApp {
	return &UserApp{
		userDomain: userDomain,
	}
}

var _ IUserApp = &UserApp{}

// Signup 用户注册
func (app *UserApp) Signup(ctx context.Context, username, passwd string) (*entity.User, error) {
	user := entity.User{
		Name: html.EscapeString(username),
	}
	user.PasswordHash = user.GenPasswordHash(passwd)

	return app.userDomain.Signup(ctx, &user)
}

// SignIn 用户登陆
func (app *UserApp) SignIn(ctx context.Context, username, passwd string) (user *entity.User, token string, err error) {
	return app.userDomain.SignIn(ctx, username, passwd)
}

func (app *UserApp) GetUserList(ctx context.Context) ([]entity.User, error) {
	return app.userDomain.GetUserList(ctx)
}
