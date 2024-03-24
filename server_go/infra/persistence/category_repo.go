package persistence

import (
	"context"
	"errors"
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

func (r *CategoryRepo) FindById(ctx context.Context, cateId uint64) (*entity.Category, error) {
	var cate entity.Category
	err := r.db.WithContext(ctx).Where("id = ?", cateId).First(&cate).Error
	if errors.Is(err, gorm.ErrRecordNotFound) {
		// 通过ID判断是否存在
		return &cate, nil
	}
	return &cate, err
}

func (r *CategoryRepo) FindByName(ctx context.Context, name string) (*entity.Category, error) {
	var cate entity.Category
	err := r.db.WithContext(ctx).Where("name = ?", name).First(&cate).Error
	if errors.Is(err, gorm.ErrRecordNotFound) {
		// 通过ID判断是否存在
		return &cate, nil
	}
	return &cate, err
}

func (r *CategoryRepo) Create(ctx context.Context, cate *entity.Category) error {
	return r.db.WithContext(ctx).Create(cate).Error
}
