package errorx

import (
	"net/http"
	"server-go/utils/renderx"
)

const (
	ErrCodeOK     = renderx.ErrCodeOK
	ErrCodeFailed = renderx.ErrCodeFailed

	ErrCodeParamInvalid = 1000
	ErrCodePermitDeny   = 1001
)

var (
	RespOK     = renderx.RespOK
	RespFailed = renderx.RespFailed

	ParamInvalid = renderx.NewRender(http.StatusOK, ErrCodeParamInvalid, "param is invalid")
	PermitDeny   = renderx.NewRender(http.StatusOK, ErrCodePermitDeny, "permission deny")
)
