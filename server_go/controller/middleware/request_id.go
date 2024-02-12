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
		requestId := uuid.New().String()
		if val, ok := c.Get(headerKeyReqId); ok {
			if reqId, ok := val.(string); ok {
				requestId = reqId
			}
		}
		c.Set(ctxKeyReqId, requestId)
		c.Next()
	}
}
