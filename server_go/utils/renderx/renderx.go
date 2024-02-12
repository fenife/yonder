package renderx

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

type Result struct {
	Code int    `json:"code"`
	Msg  string `json:"msg"`
}

type Response struct {
	Result Result      `json:"result"`
	Data   interface{} `json:"data"`
}

type Render struct {
	StatusCode int
	Response   Response
}

func NewRender(statusCode, code int, msg string, data ...interface{}) *Render {
	r := &Render{
		StatusCode: statusCode,
		Response: Response{
			Result: Result{
				Code: code,
				Msg:  msg,
			},
			Data: nil,
		},
	}
	if len(data) > 0 {
		r.Response.Data = data[0]
	}
	return r
}

const (
	ErrCodeOK     = 0
	ErrCodeFailed = 1
)

var (
	RespOK     = NewRender(http.StatusOK, ErrCodeOK, "ok")
	RespFailed = NewRender(http.StatusInternalServerError, ErrCodeFailed, "failed")
)

func ErrOutput(c *gin.Context, err interface{}) {
	r, ok := err.(*Render)
	if ok {
		c.JSON(r.StatusCode, r.Response)
		return
	}

	e, ok := err.(error)
	if ok {
		r = NewRender(http.StatusInternalServerError, ErrCodeFailed, e.Error())
		c.JSON(r.StatusCode, r.Response)
		return
	}

	c.JSON(RespFailed.StatusCode, RespFailed.Response)
	return
}

func SuccOutput(c *gin.Context, data interface{}) {
	r, ok := data.(*Render)
	if ok {
		c.JSON(r.StatusCode, r.Response)
		return
	}

	r = NewRender(http.StatusOK, ErrCodeOK, "ok", data)
	c.JSON(r.StatusCode, r.Response)
	return
}
