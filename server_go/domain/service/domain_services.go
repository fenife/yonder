package service

import (
	"server-go/domain/cache"
	"server-go/domain/repo"
)

type DomainServices struct {
	UserDomain IUserDomain
}

func NewDomainServices(
	userRepo repo.IUserRepo, userCache cache.IUserCache) *DomainServices {
	return &DomainServices{
		UserDomain: NewUserDomain(userRepo, userCache),
	}
}
