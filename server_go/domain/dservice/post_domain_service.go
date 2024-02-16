package dservice

import (
	"context"
	"server-go/domain/do"
	"server-go/domain/entity"
	"server-go/domain/repo"
	"server-go/internal/errorx"
)

type IPostDomain interface {
	GetPostStat(ctx context.Context) ([]do.PostStat, error)
	GetPostList(ctx context.Context, cateId uint64, page, limit int) ([]entity.Post, error)
	GetPostById(ctx context.Context, postId uint64) (*entity.Post, error)
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

// 获取文章详情
func (ds *PostDomain) GetPostById(ctx context.Context, postId uint64) (*entity.Post, error) {
	post, err := ds.postRepo.FindById(ctx, postId)
	if err != nil {
		return nil, err
	}
	if !post.IsValid() {
		return nil, errorx.PostNotFound
	}
	return post, nil
}
