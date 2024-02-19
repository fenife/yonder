package aservice

import (
	"context"
	"server-go/application/dto"
	"server-go/domain/do"
	"server-go/domain/dservice"
	"server-go/pkg/md2html"
)

const (
	contentTypeMd   = "md"
	contentTypeHtml = "html"
)

type IPostApp interface {
	GetPostList(ctx context.Context, cateId uint64, page, limit int) ([]*do.PostSmall, error)
	GetPostDetail(ctx context.Context, postId uint64, contentType string) (*do.PostDetail, error)
	GetPostArchiveList(ctx context.Context) ([]*dto.PostArchiveItem, error)
	GetPostAbout(ctx context.Context, contentType string) (*do.PostDetail, error)
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

func (app *PostApp) GetPostList(ctx context.Context, cateId uint64, page, limit int) ([]*do.PostSmall, error) {
	posts, err := app.postDomain.GetPostList(ctx, cateId, page, limit)
	if err != nil {
		return nil, err
	}
	postList := make([]*do.PostSmall, 0)
	for _, p := range posts {
		postList = append(postList, p.ToSmall())
	}
	return postList, err
}

func (app *PostApp) GetPostDetail(ctx context.Context, postId uint64, contentType string) (*do.PostDetail, error) {
	post, err := app.postDomain.GetPostById(ctx, postId)
	if err != nil {
		return nil, err
	}

	detail := post.ToDetail()
	switch contentType {
	case contentTypeMd:
		detail.Content = post.Content
	case contentTypeHtml:
		detail.Content = md2html.Parse(post.Content)
	}

	return detail, nil
}

func (app *PostApp) GetPostArchiveList(ctx context.Context) ([]*dto.PostArchiveItem, error) {
	posts, err := app.postDomain.GetPostArchiveList(ctx)
	if err != nil {
		return nil, err
	}
	// 默认按id倒序排序，亦即创建时间(create_at)
	yearMap := make(map[int]*dto.PostArchiveItem, 0)
	for _, v := range posts {
		p := v
		year := p.CreatedAt.Year()
		if _, ok := yearMap[year]; !ok {
			yearMap[year] = &dto.PostArchiveItem{
				Year:     year,
				Count:    0,
				PostList: make([]*do.PostDetail, 0),
			}
		}
		detail := p.ToDetail()

		yearMap[year].PostList = append(yearMap[year].PostList, detail)
		yearMap[year].Count += 1
	}

	result := make([]*dto.PostArchiveItem, 0)
	for _, v := range yearMap {
		p := v
		result = append(result, p)
	}
	return result, err
}

func (app *PostApp) GetPostAbout(ctx context.Context, contentType string) (*do.PostDetail, error) {
	post, err := app.postDomain.GetPostAbout(ctx)
	if err != nil {
		return nil, err
	}

	detail := post.ToDetail()
	detail.Content = post.Content

	return detail, nil
}
