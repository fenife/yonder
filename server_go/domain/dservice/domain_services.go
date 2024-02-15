package dservice

import (
	"server-go/domain/cache"
	"server-go/domain/repo"
)

type DomainServices struct {
	UserDomain     IUserDomain
	CategoryDomain ICategoryDomain
}

func NewDomainServices(
	userRepo repo.IUserRepo, userCache cache.IUserCache, cateRepo repo.ICategoryRepo,
) *DomainServices {
	return &DomainServices{
		UserDomain:     NewUserDomain(userRepo, userCache),
		CategoryDomain: NewCategoryDomain(cateRepo),
	}
}
