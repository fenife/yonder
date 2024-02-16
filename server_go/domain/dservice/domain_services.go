package dservice

import (
	"server-go/domain/cache"
	"server-go/domain/repo"
)

type DomainServices struct {
	UserDomain     IUserDomain
	CategoryDomain ICategoryDomain
	PostDomain     IPostDomain
}

func NewDomainServices(
	userRepo repo.IUserRepo, userCache cache.IUserCache, cateRepo repo.ICategoryRepo, postRepo repo.IPostRepo,
) *DomainServices {
	return &DomainServices{
		UserDomain:     NewUserDomain(userRepo, userCache),
		CategoryDomain: NewCategoryDomain(cateRepo),
		PostDomain:     NewPostDomain(postRepo),
	}
}
