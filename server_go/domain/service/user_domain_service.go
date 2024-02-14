package service

import (
	"context"
	"server-go/domain/cache"
	"server-go/domain/entity"
	"server-go/domain/repo"
	"server-go/internal/errorx"
	"server-go/pkg/logx"
)

type IUserDomain interface {
	Signup(ctx context.Context, user *entity.User) (*entity.User, error)
	FindByName(ctx context.Context, name string) (*entity.User, error)
	FindById(ctx context.Context, userId uint64) (*entity.User, error)
	UserExisted(ctx context.Context, name string) (bool, error)
	GetUserList(ctx context.Context) ([]entity.User, error)
	SignIn(ctx context.Context, name, password string) (user *entity.User, token string, err error)
	FindByToken(ctx context.Context, userToken string) (*entity.User, error)
}

type UserDomain struct {
	userRepo  repo.IUserRepo
	userCache cache.IUserCache
}

func NewUserDomain(userRepo repo.IUserRepo, userCache cache.IUserCache) *UserDomain {
	return &UserDomain{
		userRepo:  userRepo,
		userCache: userCache,
	}
}

var _ IUserDomain = &UserDomain{}

func (ds *UserDomain) Signup(ctx context.Context, user *entity.User) (*entity.User, error) {
	// 用户已经存在
	existed, err := ds.UserExisted(ctx, user.Name)
	if err != nil {
		return nil, err
	}
	if existed {
		return nil, errorx.UserExisted
	}

	return ds.userRepo.CreateUser(ctx, user)
}

func (ds *UserDomain) UserExisted(ctx context.Context, name string) (bool, error) {
	user, err := ds.userRepo.FindByName(ctx, name)
	if err != nil {
		return false, err
	}
	if user.ID <= 0 {
		return false, nil
	}
	return true, nil
}

func (ds *UserDomain) FindByName(ctx context.Context, name string) (*entity.User, error) {
	return ds.userRepo.FindByName(ctx, name)
}

func (ds *UserDomain) FindById(ctx context.Context, userId uint64) (*entity.User, error) {
	return ds.userRepo.FindById(ctx, userId)
}

func (ds *UserDomain) GetUserList(ctx context.Context) ([]entity.User, error) {
	return ds.userRepo.GetUserList(ctx)
}

func (ds *UserDomain) FindByToken(ctx context.Context, userToken string) (*entity.User, error) {
	return nil, nil
}

func (ds *UserDomain) SignIn(ctx context.Context, name, password string) (user *entity.User, token string, err error) {
	// 查找用户
	user, err = ds.userRepo.FindByName(ctx, name)
	if err != nil {
		return nil, "", err
	}
	// 检查用户是否存在
	if !user.IsValid() {
		return nil, "", errorx.UserNotExisted
	}
	// 检查密码是否错误
	pwHash := user.GenPasswordHash(password)
	if user.PasswordHash != pwHash {
		logx.Ctx(ctx).Errorf("password is not valid: %s != %s", user.PasswordHash, pwHash)
		return nil, "", errorx.UserNameOrPasswdNotValid
	}
	// 检查是否已经登陆
	u, err := ds.userCache.GetUserById(ctx, user.ID)
	if err != nil {
		return nil, "", err
	}
	if u.IsValid() {
		return nil, "", errorx.UserAlreadySignIn
	}
	// 生成用户token
	token = user.GenUserToken()
	// 缓存用户信息
	if err = ds.userCache.CacheUserByToken(ctx, token, user); err != nil {
		return nil, "", err
	}
	return
}
