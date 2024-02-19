package repo

import (
	"context"
	"server-go/domain/do"
	"server-go/domain/entity"
)

type IPostRepo interface {
	GetPostStat(ctx context.Context) ([]do.PostStat, error)
	GetPostList(ctx context.Context, cateId uint64, page, limit int) ([]entity.Post, error)
	FindById(ctx context.Context, postId uint64) (*entity.Post, error)
	GetPostArchiveList(ctx context.Context) ([]*entity.Post, error)
	FindByTitle(ctx context.Context, name string) (*entity.Post, error)
}