package aservice

import (
	"context"
	"server-go/application/dto"
	"server-go/domain/do"
	"server-go/domain/dservice"
	"server-go/domain/entity"
)

type ICategoryApp interface {
	GetCategoryList(ctx context.Context) ([]dto.CategoryList, error)
}

type CategoryApp struct {
	categoryDomain dservice.ICategoryDomain
	postDomain     dservice.IPostDomain
}

func NewCategoryApp(categoryDomain dservice.ICategoryDomain, postDomain dservice.IPostDomain) *CategoryApp {
	return &CategoryApp{
		categoryDomain: categoryDomain,
		postDomain:     postDomain,
	}
}

var _ ICategoryApp = &CategoryApp{}

func (app *CategoryApp) GetCategoryList(ctx context.Context) ([]dto.CategoryList, error) {
	cates, err := app.categoryDomain.GetCategoryList(ctx)
	if err != nil {
		return nil, err
	}
	postStat, err := app.postDomain.GetPostStat(ctx)
	if err != nil {
		return nil, err
	}

	// list -> map
	statMaps := make(map[uint64]do.PostStat, 0)
	for _, p := range postStat {
		statMaps[p.CateId] = p
	}

	res := make([]dto.CategoryList, 0)
	for _, c := range cates {
		d := dto.CategoryList{
			CateId:   c.ID,
			CateName: c.Name,
		}
		// 该分类下可展示文章的数目
		if p, ok := statMaps[c.ID]; ok {
			d.PostCount = p.PostCount
		}
		res = append(res, d)
	}
	return res, nil
}

func cateToBrief(cate *entity.Category) dto.CategoryBrief {
	c := dto.CategoryBrief{
		ID:        cate.ID,
		CreatedAt: cate.CreatedAt.Format(timeFormatLayout),
		UpdatedAt: cate.CreatedAt.Format(timeFormatLayout),
		Name:      cate.Name,
	}
	return c
}
