package aservice

import (
	"context"
	"server-go/application/dto"
	"server-go/domain/dservice"
	"server-go/domain/entity"
)

type IPostApp interface {
	GetPostList(ctx context.Context, cateId uint64, page, limit int) ([]dto.PostBrief, error)
	GetPostDetail(ctx context.Context, postId uint64, contentType string) (*dto.PostDetail, error)
}

type PostApp struct {
	postDomain dservice.IPostDomain
	cateDomain dservice.ICategoryDomain
	userDomain dservice.IUserDomain
}

func NewPostApp(postDomain dservice.IPostDomain, cateDomain dservice.ICategoryDomain,
	userDomain dservice.IUserDomain) *PostApp {
	return &PostApp{
		postDomain: postDomain,
		cateDomain: cateDomain,
		userDomain: userDomain,
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
		postList = append(postList, postToBrief(&p))
	}
	return postList, err
}

func postToBrief(post *entity.Post) dto.PostBrief {
	p := dto.PostBrief{
		ID:        post.ID,
		CreatedAt: post.CreatedAt.Format(timeFormatLayout),
		UpdatedAt: post.CreatedAt.Format(timeFormatLayout),
		UserId:    post.UserId,
		CateId:    post.CateId,
		Title:     post.Title,
		TitleEn:   post.TitleEn,
	}
	return p
}

func (app *PostApp) GetPostDetail(ctx context.Context, postId uint64, contentType string) (*dto.PostDetail, error) {
	post, err := app.postDomain.GetPostById(ctx, postId)
	if err != nil {
		return nil, err
	}

	detail := dto.PostDetail{
		PostBrief: postToBrief(post),
		User:      userToBrief(&post.User),
		Category:  cateToBrief(&post.Category),
	}
	detail.Content = post.Content // todo: markdown to html
	return &detail, nil
}
