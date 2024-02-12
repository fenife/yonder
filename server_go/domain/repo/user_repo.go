package repo

import (
	"context"
	"server-go/domain/entity"
)

type IUserRepo interface {
	CreateUser(ctx context.Context, user *entity.User) (*entity.User, error)
	GetUserList(ctx context.Context) ([]entity.User, error)
}
