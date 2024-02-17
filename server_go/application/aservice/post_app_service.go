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
	GetPostArchiveList(ctx context.Context) ([]*dto.PostArchiveItem, error)
	GetPostAbout(ctx context.Context, contentType string) (*dto.PostDetail, error)
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

	detail := postToDetail(post)
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
				PostList: make([]*dto.PostDetail, 0),
			}
		}
		detail := &dto.PostDetail{
			PostBrief: postToBrief(p),
			User:      userToBrief(&p.User),
			Category:  cateToBrief(&p.Category),
		}

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

func (app *PostApp) GetPostAbout(ctx context.Context, contentType string) (*dto.PostDetail, error) {
	post, err := app.postDomain.GetPostAbout(ctx)
	if err != nil {
		return nil, err
	}
	detail := postToDetail(post)
	return detail, nil
}

func postToDetail(post *entity.Post) *dto.PostDetail {
	detail := dto.PostDetail{
		PostBrief: postToBrief(post),
		User:      userToBrief(&post.User),
		Category:  cateToBrief(&post.Category),
	}
	detail.Content = post.Content // todo: markdown to html
	return &detail
}
