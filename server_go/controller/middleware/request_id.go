package middleware

import (
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"server-go/internal/gctx"
)

const HeaderKeyReqId = "X-Request-Id"

func AddRequestId() gin.HandlerFunc {
	return func(c *gin.Context) {
		reqId := c.GetHeader(HeaderKeyReqId)
		if reqId == "" {
			reqId = uuid.New().String()
		}
		gctx.SetReqId(c, reqId)

		// 在响应头中也返回 request id
		c.Writer.Header().Set(HeaderKeyReqId, reqId)

		c.Next()
	}
}
