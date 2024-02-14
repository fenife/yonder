package application

import "server-go/domain/service"

type Apps struct {
	UserApp IUserApp
}

func NewApps(userDomain service.IUserDomain) *Apps {
	return &Apps{
		UserApp: NewUserApp(userDomain),
	}
}
