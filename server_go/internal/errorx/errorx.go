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

	// 用户注册
	ErrCodeUserSignupFailed = 2001
	ErrCodeUserExisted      = 2002
	// 用户登陆
	ErrCodeUserSignInFailed         = 2101
	ErrCodeUserNotExisted           = 2102
	ErrCodeUserNameOrPasswdNotValid = 2103
	ErrCodeUserAlreadySignIn        = 2104

	//ErrCodePermitDeny = 1101
)

var (
	RespOK     = renderx.RespOK
	RespFailed = renderx.RespFailed

	// 通用
	ParamInvalid = renderx.NewRender(http.StatusOK, ErrCodeParamInvalid, "param is invalid")

	// 用户注册
	UserSignupFailed = renderx.NewRender(http.StatusOK, ErrCodeUserSignupFailed, "user sign up failed")
	UserExisted      = renderx.NewRender(http.StatusOK, ErrCodeUserExisted, "user existed")
	// 用户登陆
	UserSignInFailed         = renderx.NewRender(http.StatusOK, ErrCodeUserSignInFailed, "user sign in failed")
	UserNotExisted           = renderx.NewRender(http.StatusOK, ErrCodeUserNotExisted, "user not existed")
	UserNameOrPasswdNotValid = renderx.NewRender(http.StatusOK, ErrCodeUserNameOrPasswdNotValid, "user name or password not valid")
	UserAlreadySignIn        = renderx.NewRender(http.StatusOK, ErrCodeUserAlreadySignIn, "user already sign in")

	//PermitDeny = renderx.NewRender(http.StatusOK, ErrCodePermitDeny, "user permission deny")
)
