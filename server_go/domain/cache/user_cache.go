package cache

import (
	"context"
	"server-go/domain/entity"
)

type IUserCache interface {
	CacheUserSignInInfo(ctx context.Context, user *entity.User, signin *entity.UserSignInInfo) error
	GetUserByToken(ctx context.Context, token string) (*entity.User, error)
	GetUserById(ctx context.Context, userId uint64) (*entity.User, error)
	DelUserSignInByToken(ctx context.Context, token string) error
	GetUserSignInInfo(ctx context.Context, userId uint64) (*entity.UserSignInInfo, error)
}
