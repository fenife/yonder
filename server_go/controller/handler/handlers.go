package handler

import (
	"server-go/application/service"
)

type Handlers struct {
	PingHandler *PingHandler
	UserHandler *UserHandler
}

func NewHandlers(userApp service.IUserApp) *Handlers {
	return &Handlers{
		PingHandler: NewPingHandler(),
		UserHandler: NewUserHandler(userApp),
	}
}
