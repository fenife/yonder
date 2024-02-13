package application

import (
	"context"
	"html"
	"server-go/domain/entity"
	"server-go/domain/service"
	"server-go/pkg/utils"
)

type IUserApp interface {
	CreateUser(ctx context.Context, username, passwd string) (*entity.User, error)
	GetUserList(ctx context.Context) ([]entity.User, error)
}

type UserApp struct {
	userDomainService service.IUserDomainService
}

func NewUserApp(userDomainService service.IUserDomainService) *UserApp {
	return &UserApp{
		userDomainService: userDomainService,
	}
}

var _ IUserApp = &UserApp{}

func (app *UserApp) CreateUser(ctx context.Context, username, passwd string) (*entity.User, error) {
	user := entity.User{
		Name:         html.EscapeString(username),
		PasswordHash: utils.Md5(passwd),
	}
	return app.userDomainService.CreateUser(ctx, &user)
}

func (app *UserApp) GetUserList(ctx context.Context) ([]entity.User, error) {
	return app.userDomainService.GetUserList(ctx)
}
