package middleware

import (
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"server-go/internal/gctx"
)

const (
	headerKeyReqId = "x-request-id"
)

func RequestIdMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		reqId := c.GetHeader(headerKeyReqId)
		if reqId == "" {
			reqId = uuid.New().String()
		}
		gctx.SetReqId(c, reqId)
		c.Next()
	}
}
