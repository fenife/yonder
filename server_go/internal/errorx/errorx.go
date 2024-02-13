package errorx

import (
	"net/http"
	"server-go/pkg/renderx"
)

const (
	ErrCodeOK     = renderx.ErrCodeOK
	ErrCodeFailed = renderx.ErrCodeFailed

	// 通用
	ErrCodeParamInvalid = 1001

	// 用户
	ErrCodeUserSignupFailed = 2001
	ErrCodeUserExisted      = 2002

	//ErrCodePermitDeny = 1101
)

var (
	RespOK     = renderx.RespOK
	RespFailed = renderx.RespFailed

	// 通用
	ParamInvalid = renderx.NewRender(http.StatusOK, ErrCodeParamInvalid, "param is invalid")

	// 用户
	UserSignupFailed = renderx.NewRender(http.StatusOK, ErrCodeUserSignupFailed, "user sign up failed")
	UserExisted      = renderx.NewRender(http.StatusOK, ErrCodeUserExisted, "user existed")

	//PermitDeny = renderx.NewRender(http.StatusOK, ErrCodePermitDeny, "user permission deny")
)
