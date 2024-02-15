package application

import "server-go/domain/service"

type Apps struct {
	UserApp     IUserApp
	CategoryApp ICategoryApp
}

func NewApps(userDomain service.IUserDomain, categoryDomain service.ICategoryDomain) *Apps {
	return &Apps{
		UserApp:     NewUserApp(userDomain),
		CategoryApp: NewCategoryApp(categoryDomain),
	}
}
