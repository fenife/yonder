package service

import (
	"server-go/domain/cache"
	"server-go/domain/repo"
)

type DomainServices struct {
	UserDomainService IUserDomainService
}

func NewDomainServices(
	userRepo repo.IUserRepo, userCache cache.IUserCache) *DomainServices {
	return &DomainServices{
		UserDomainService: NewUserDomainService(userRepo, userCache),
	}
}
