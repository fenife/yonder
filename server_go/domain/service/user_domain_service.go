package service

import (
	"context"
	"server-go/domain/entity"
	"server-go/domain/repo"
	"server-go/internal/errorx"
)

type IUserDomainService interface {
	CreateUser(ctx context.Context, user *entity.User) (*entity.User, error)
	UserExisted(ctx context.Context, name string) (bool, error)
	GetUserList(ctx context.Context) ([]entity.User, error)
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

func (ds *UserDomainService) CreateUser(ctx context.Context, user *entity.User) (*entity.User, error) {
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

func (ds *UserDomainService) GetUserList(ctx context.Context) ([]entity.User, error) {
	return ds.userRepo.GetUserList(ctx)
}
