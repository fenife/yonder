package dservice

import (
	"context"
	"server-go/domain/entity"
	"server-go/domain/repo"
	"server-go/internal/errorx"
)

type ICategoryDomain interface {
	GetCategoryList(ctx context.Context) ([]entity.Category, error)
	GetCategoryById(ctx context.Context, cateId uint64) (*entity.Category, error)
}

type CategoryDomain struct {
	cateRepo repo.ICategoryRepo
}

func NewCategoryDomain(cateRepo repo.ICategoryRepo) *CategoryDomain {
	return &CategoryDomain{
		cateRepo: cateRepo,
	}
}

var _ ICategoryDomain = &CategoryDomain{}

func (ds *CategoryDomain) GetCategoryList(ctx context.Context) ([]entity.Category, error) {
	return ds.cateRepo.GetCategoryList(ctx)
}

// 获取分类详情
func (ds *CategoryDomain) GetCategoryById(ctx context.Context, cateId uint64) (*entity.Category, error) {
	cate, err := ds.cateRepo.FindById(ctx, cateId)
	if err != nil {
		return nil, err
	}
	if !cate.IsValid() {
		return nil, errorx.CategoryNotFound
	}
	return cate, nil
}
