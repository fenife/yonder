package aservice

import (
	"context"
	"server-go/domain/dservice"
	"server-go/domain/entity"
)

type ICategoryApp interface {
	GetCategoryList(ctx context.Context) ([]entity.Category, error)
}

type CategoryApp struct {
	categoryDomain dservice.ICategoryDomain
}

func NewCategoryApp(categoryDomain dservice.ICategoryDomain) *CategoryApp {
	return &CategoryApp{
		categoryDomain: categoryDomain,
	}
}

var _ ICategoryApp = &CategoryApp{}

func (app *CategoryApp) GetCategoryList(ctx context.Context) ([]entity.Category, error) {
	return app.categoryDomain.GetCategoryList(ctx)
}
