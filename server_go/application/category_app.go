package application

import (
	"context"
	"server-go/domain/entity"
	"server-go/domain/service"
)

type ICategoryApp interface {
	GetCategoryList(ctx context.Context) ([]entity.Category, error)
}

type CategoryApp struct {
	categoryDomain service.ICategoryDomain
}

func NewCategoryApp(categoryDomain service.ICategoryDomain) *CategoryApp {
	return &CategoryApp{
		categoryDomain: categoryDomain,
	}
}

var _ ICategoryApp = &CategoryApp{}

func (app *CategoryApp) GetCategoryList(ctx context.Context) ([]entity.Category, error) {
	return app.categoryDomain.GetCategoryList(ctx)
}
