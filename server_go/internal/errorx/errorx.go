package errorx

import (
	"net/http"
	"server-go/utils/renderx"
)

const (
	ErrCodeOK     = renderx.ErrCodeOK
	ErrCodeFailed = renderx.ErrCodeFailed

	ErrCodeParamInvalid = 100
)

var (
	RespOK     = renderx.RespOK
	RespFailed = renderx.RespFailed

	ParamInvalid = renderx.NewRender(http.StatusOK, ErrCodeParamInvalid, "param is invalid")
)
