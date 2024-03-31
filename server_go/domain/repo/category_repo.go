package repo

import (
	"context"
	"server-go/domain/entity"
)

type ICategoryRepo interface {
	GetCategoryList(ctx context.Context) ([]entity.Category, error)
	FindById(ctx context.Context, cateId uint64) (*entity.Category, error)
	FindByName(ctx context.Context, name string) (*entity.Category, error)
	Create(ctx context.Context, cate *entity.Category) error
	Update(ctx context.Context, cateId uint64, fields map[string]interface{}) error
}
