package aservice

import (
	"server-go/domain/dservice"
)

type Apps struct {
	UserApp     IUserApp
	CategoryApp ICategoryApp
}

func NewApps(userDomain dservice.IUserDomain, categoryDomain dservice.ICategoryDomain) *Apps {
	return &Apps{
		UserApp:     NewUserApp(userDomain),
		CategoryApp: NewCategoryApp(categoryDomain),
	}
}
