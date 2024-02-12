package persistence

import (
	"context"
	"gorm.io/gorm"
	"server-go/domain/entity"
	"server-go/domain/repo"
)

type UserRepo struct {
	db *gorm.DB
}

func NewUserRepo(db *gorm.DB) *UserRepo {
	return &UserRepo{db}
}

// UserRepo implements the repository.UserRepository interface
var _ repo.IUserRepo = &UserRepo{}

func (repo *UserRepo) CreateUser(ctx context.Context, user *entity.User) (*entity.User, error) {
	err := repo.db.WithContext(ctx).Create(&user).Error
	return user, err
}

func (repo *UserRepo) GetUserList(ctx context.Context) ([]entity.User, error) {
	var users []entity.User
	err := repo.db.WithContext(ctx).Find(&users).Error
	return users, err
}
