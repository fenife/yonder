package handler

import "server-go/application"

type Handlers struct {
	PingHandler *PingHandler
	UserHandler *UserHandler
}

func NewHandlers(userApp application.IUserApp) *Handlers {
	return &Handlers{
		PingHandler: NewPingHandler(),
		UserHandler: NewUserHandler(userApp),
	}
}
