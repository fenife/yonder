package aservice

import (
	"context"
	"server-go/domain/dservice"
	"server-go/domain/entity"
)

type IPostApp interface {
	GetPostList(ctx context.Context, cateId uint64, page, limit int) ([]entity.Post, error)
}

type PostApp struct {
	postDomain dservice.IPostDomain
}

func NewPostApp(postDomain dservice.IPostDomain) *PostApp {
	return &PostApp{
		postDomain: postDomain,
	}
}

var _ IPostApp = &PostApp{}

func (app *PostApp) GetPostList(ctx context.Context, cateId uint64, page, limit int) ([]entity.Post, error) {
	return app.postDomain.GetPostList(ctx, cateId, page, limit)
}
