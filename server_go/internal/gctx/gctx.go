package gctx

import (
	"context"
	"github.com/gin-gonic/gin"
	"server-go/domain/entity"
)

const (
	ctxKeyReqId = "request_id"
	ctxKeyUser  = "user"
)

func SetReqId(ctx *gin.Context, reqId string) {
	ctx.Set(ctxKeyReqId, reqId)
}

func GetReqId(ctx context.Context) (reqId string) {
	if val := ctx.Value(ctxKeyReqId); val != nil {
		reqId, _ = val.(string)
	}
	return
}

func SetUser(ctx *gin.Context, user *entity.User) {
	ctx.Set(ctxKeyUser, user)
}

func GetUser(ctx context.Context) (user *entity.User) {
	if val := ctx.Value(ctxKeyUser); val != nil {
		user, _ = val.(*entity.User)
	}
	return
}
