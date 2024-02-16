package aservice

import (
	"context"
	"server-go/application/dto"
	"server-go/domain/dservice"
	"server-go/domain/entity"
)

type IPostApp interface {
	GetPostList(ctx context.Context, cateId uint64, page, limit int) ([]dto.PostBrief, error)
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

func (app *PostApp) GetPostList(ctx context.Context, cateId uint64, page, limit int) ([]dto.PostBrief, error) {
	posts, err := app.postDomain.GetPostList(ctx, cateId, page, limit)
	if err != nil {
		return nil, err
	}
	postList := make([]dto.PostBrief, 0)
	for _, p := range posts {
		postList = append(postList, getPostDto(&p))
	}
	return postList, err
}

func getPostDto(post *entity.Post) dto.PostBrief {
	layout := "2006-01-02 15:05:05"
	p := dto.PostBrief{
		ID:        post.ID,
		CreatedAt: post.CreatedAt.Format(layout),
		UpdatedAt: post.CreatedAt.Format(layout),
		UserId:    post.UserId,
		CateId:    post.CateId,
		Title:     post.Title,
		TitleEn:   post.TitleEn,
		Content:   post.Content,
	}
	return p
}
