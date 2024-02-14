package service

import (
	"context"
	"server-go/domain/entity"
	"server-go/domain/repo"
	"server-go/internal/errorx"
	"server-go/pkg/logx"
)

type IUserDomainService interface {
	Signup(ctx context.Context, user *entity.User) (*entity.User, error)
	FindByName(ctx context.Context, name string) (*entity.User, error)
	FindById(ctx context.Context, userId uint64) (*entity.User, error)
	UserExisted(ctx context.Context, name string) (bool, error)
	GetUserList(ctx context.Context) ([]entity.User, error)
	SignIn(ctx context.Context, name, password string) (user *entity.User, token string, err error)
	FindByToken(ctx context.Context, userToken string) (*entity.User, error)
}

type UserDomainService struct {
	userRepo repo.IUserRepo
}

func NewUserDomainService(userRepo repo.IUserRepo) *UserDomainService {
	return &UserDomainService{
		userRepo: userRepo,
	}
}

var _ IUserDomainService = &UserDomainService{}

func (ds *UserDomainService) Signup(ctx context.Context, user *entity.User) (*entity.User, error) {
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

func (ds *UserDomainService) UserExisted(ctx context.Context, name string) (bool, error) {
	user, err := ds.userRepo.FindByName(ctx, name)
	if err != nil {
		return false, err
	}
	if user.ID <= 0 {
		return false, nil
	}
	return true, nil
}

func (ds *UserDomainService) FindByName(ctx context.Context, name string) (*entity.User, error) {
	return ds.userRepo.FindByName(ctx, name)
}

func (ds *UserDomainService) FindById(ctx context.Context, userId uint64) (*entity.User, error) {
	return ds.userRepo.FindById(ctx, userId)
}

func (ds *UserDomainService) GetUserList(ctx context.Context) ([]entity.User, error) {
	return ds.userRepo.GetUserList(ctx)
}

func (ds *UserDomainService) FindByToken(ctx context.Context, userToken string) (*entity.User, error) {
	return nil, nil
}

func (ds *UserDomainService) SignIn(ctx context.Context, name, password string) (user *entity.User, token string, err error) {
	// todo: 检查用户是否已经登陆

	// 查找用户
	user, err = ds.userRepo.FindByName(ctx, name)
	if err != nil {
		return nil, "", err
	}
	// 检查用户是否存在或是否已删除
	if user.ID <= 0 {
		return nil, "", errorx.UserNotExisted
	}
	// 检查密码是否错误
	pwHash := user.GenPasswordHash(password)
	if user.PasswordHash != pwHash {
		logx.Ctx(ctx).Errorf("password is not valid: %s != %s", user.PasswordHash, pwHash)
		return nil, "", errorx.UserNameOrPasswdNotValid
	}
	// 生成用户token
	token = user.GenUserToken()

	// todo: 缓存

	return
}
