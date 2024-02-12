package middleware

import (
	"bytes"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"io"
	"server-go/utils/logx"
)

func LogContext() gin.HandlerFunc {
	return func(c *gin.Context) {
		requestId := uuid.New().String()
		c.Set(ctxKeyReqId, requestId)

		// req
		body, _ := io.ReadAll(c.Request.Body)
		println(string(body))

		c.Request.Body = io.NopCloser(bytes.NewReader(body))

		c.Next()

		// resp
		logx.Ctx(c).Infof("log context")
	}
}
