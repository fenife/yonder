package middleware

import (
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

const (
	headerKeyReqId = "x-request-id"
	ctxKeyReqId    = "request_id"
)

func RequestIdMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		reqId := c.GetHeader(headerKeyReqId)
		if reqId == "" {
			reqId = uuid.New().String()
		}
		c.Set(ctxKeyReqId, reqId)
		c.Next()
	}
}
