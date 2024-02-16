package aservice

import (
	"server-go/domain/dservice"
)

type Apps struct {
	UserApp     IUserApp
	CategoryApp ICategoryApp
	PostApp     IPostApp
}

func NewApps(userDomain dservice.IUserDomain, categoryDomain dservice.ICategoryDomain, postDomain dservice.IPostDomain) *Apps {
	return &Apps{
		UserApp:     NewUserApp(userDomain),
		CategoryApp: NewCategoryApp(categoryDomain, postDomain),
		PostApp:     NewPostApp(postDomain),
	}
}
