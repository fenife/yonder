package repo

import (
	"context"
	"server-go/domain/do"
	"server-go/domain/entity"
)

type IPostRepo interface {
	GetPostStat(ctx context.Context) ([]do.PostStat, error)
	GetPostList(ctx context.Context, cateId uint64, page, limit int) ([]entity.Post, error)
}
