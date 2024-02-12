package application

import (
	"context"
	"server-go/domain/entity"
	"server-go/domain/repo"
)

type IUserApp interface {
	CreateUser(ctx context.Context, user *entity.User) (*entity.User, error)
	GetUserList(ctx context.Context) ([]entity.User, error)
}

type UserApp struct {
	userRepo repo.IUserRepo
}

func NewUserApp(userRepo repo.IUserRepo) *UserApp {
	return &UserApp{
		userRepo: userRepo,
	}
}

var _ IUserApp = &UserApp{}

func (app *UserApp) CreateUser(ctx context.Context, user *entity.User) (*entity.User, error) {
	return app.userRepo.CreateUser(ctx, user)
}

func (app *UserApp) GetUserList(ctx context.Context) ([]entity.User, error) {
	return app.userRepo.GetUserList(ctx)
}
