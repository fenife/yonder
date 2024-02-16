package dservice

import (
	"context"
	"server-go/domain/do"
	"server-go/domain/entity"
	"server-go/domain/repo"
)

type IPostDomain interface {
	GetPostStat(ctx context.Context) ([]do.PostStat, error)
	GetPostList(ctx context.Context, cateId uint64, page, limit int) ([]entity.Post, error)
}

type PostDomain struct {
	postRepo repo.IPostRepo
}

func NewPostDomain(postRepo repo.IPostRepo) *PostDomain {
	return &PostDomain{
		postRepo: postRepo,
	}
}

var _ IPostDomain = &PostDomain{}

// 按分类获取文章数目
func (ds *PostDomain) GetPostStat(ctx context.Context) ([]do.PostStat, error) {
	return ds.postRepo.GetPostStat(ctx)
}

// 获取文章列表
func (ds *PostDomain) GetPostList(ctx context.Context, cateId uint64, page, limit int) ([]entity.Post, error) {
	return ds.postRepo.GetPostList(ctx, cateId, page, limit)
}
