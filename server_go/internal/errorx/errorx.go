package errorx

import (
	"net/http"
	"server-go/pkg/renderx"
)

const (
	ErrCodeOK     = renderx.ErrCodeOK
	ErrCodeFailed = renderx.ErrCodeFailed

	// 通用
	errCodeParamInvalid = 1001

	// 用户注册
	errCodeUserSignupFailed = 2001
	errCodeUserExisted      = 2002
	// 用户登陆
	errCodeUserSignInFailed         = 2101
	errCodeUserNotExisted           = 2102
	errCodeUserNameOrPasswdNotValid = 2103
	errCodeUserAlreadySignIn        = 2104
	errCodeUserAuthFailed           = 2105

	//ErrCodePermitDeny = 1101
)

var (
	RespOK     = renderx.RespOK
	RespFailed = renderx.RespFailed

	// 通用
	ParamInvalid = renderx.NewRender(http.StatusOK, errCodeParamInvalid, "param is invalid")

	// 用户注册
	UserSignupFailed = renderx.NewRender(http.StatusOK, errCodeUserSignupFailed, "user sign up failed")
	UserExisted      = renderx.NewRender(http.StatusOK, errCodeUserExisted, "user existed")
	// 用户登陆
	UserSignInFailed         = renderx.NewRender(http.StatusOK, errCodeUserSignInFailed, "user sign in failed")
	UserNotExisted           = renderx.NewRender(http.StatusOK, errCodeUserNotExisted, "user not existed")
	UserNameOrPasswdNotValid = renderx.NewRender(http.StatusOK, errCodeUserNameOrPasswdNotValid, "user name or password not valid")
	UserAlreadySignIn        = renderx.NewRender(http.StatusOK, errCodeUserAlreadySignIn, "user already sign in")
	UserAuthFailed           = renderx.NewRender(http.StatusOK, errCodeUserAuthFailed, "user auth failed")

	//PermitDeny = renderx.NewRender(http.StatusOK, ErrCodePermitDeny, "user permission deny")
)
