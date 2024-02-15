package dservice

import (
	"context"
	"server-go/domain/entity"
	"server-go/domain/repo"
)

type ICategoryDomain interface {
	GetCategoryList(ctx context.Context) ([]entity.Category, error)
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
