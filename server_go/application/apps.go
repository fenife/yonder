package application

import "server-go/domain/service"

type Apps struct {
	UserApp IUserApp
}

func NewApps(userDomainService service.IUserDomainService) *Apps {
	return &Apps{
		UserApp: NewUserApp(userDomainService),
	}
}
