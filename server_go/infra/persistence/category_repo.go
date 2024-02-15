package persistence

import (
	"context"
	"gorm.io/gorm"
	"server-go/domain/entity"
	"server-go/domain/repo"
)

type CategoryRepo struct {
	db *gorm.DB
}

func NewCategoryRepo(db *gorm.DB) *CategoryRepo {
	return &CategoryRepo{db}
}

// UserRepo implements the repo.UserRepo interface
var _ repo.ICategoryRepo = &CategoryRepo{}

func (r *CategoryRepo) GetCategoryList(ctx context.Context) ([]entity.Category, error) {
	var cates []entity.Category
	err := r.db.WithContext(ctx).Find(&cates).Error
	return cates, err
}
