package middleware

import (
	"bytes"
	"github.com/gin-gonic/gin"
	"io"
	"server-go/utils/logx"
	"time"
)

type bodyLogWriter struct {
	gin.ResponseWriter
	body *bytes.Buffer
}

func (w bodyLogWriter) Write(b []byte) (int, error) {
	w.body.Write(b)
	return w.ResponseWriter.Write(b)
}

func LogContext() gin.HandlerFunc {
	return func(c *gin.Context) {
		t := time.Now()
		// 获取请求body数据
		bodyData, _ := io.ReadAll(c.Request.Body)
		c.Request.Body = io.NopCloser(bytes.NewReader(bodyData))

		// 双写
		writer := &bodyLogWriter{body: bytes.NewBufferString(""), ResponseWriter: c.Writer}
		c.Writer = writer

		// 请求处理
		c.Next()

		// log记录请求和响应
		withArgs := []interface{}{
			"method", c.Request.Method,
			"path", c.Request.RequestURI,
			"body", string(bodyData),
			"internal", time.Since(t).Milliseconds(), // 毫秒
			"status", c.Writer.Status(),
			"response", writer.body.String(),
		}
		logx.Ctx(c).With(withArgs...).Infof("")
	}
}
