package cache

import (
	"context"
	"server-go/domain/entity"
)

type IUserCache interface {
	CacheUserByToken(ctx context.Context, token string, user *entity.User) error
	GetUserByToken(ctx context.Context, token string) (*entity.User, error)
	GetUserById(ctx context.Context, userId uint64) (*entity.User, error)
}
