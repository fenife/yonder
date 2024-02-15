package repo

import (
	"context"
	"server-go/domain/entity"
)

type ICategoryRepo interface {
	GetCategoryList(ctx context.Context) ([]entity.Category, error)
}
