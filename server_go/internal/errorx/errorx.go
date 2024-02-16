package errorx

import (
	"net/http"
	"server-go/pkg/renderx"
)

const (
	ErrCodeOK     = renderx.ErrCodeOK
	ErrCodeFailed = renderx.ErrCodeFailed

	// 通用 11-10-xx
	errCodeParamInvalid = 111001

	// 用户 12-xx-xx
	// 用户注册 12-10-xx
	errCodeUserSignupFailed = 121001
	errCodeUserExisted      = 121002
	// 用户登陆 12-11-xx
	errCodeUserSignInFailed         = 121101
	errCodeUserNotExisted           = 121102
	errCodeUserNameOrPasswdNotValid = 121103
	errCodeUserAlreadySignIn        = 121104
	errCodeUserAuthFailed           = 121105
	// 用户退出 12-12-xx
	errCodeUserSignOutFailed = 121201

	//ErrCodePermitDeny = 1101

	// 文章分类 13-xx-xx
	errCodeGetCateListFailed = 131101

	// 文章 15-xx-xx
	errCodeGetPostListFailed = 151101
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
	// 用户退出
	UserSignOutFailed = renderx.NewRender(http.StatusOK, errCodeUserSignOutFailed, "user sign out failed")

	//PermitDeny = renderx.NewRender(http.StatusOK, ErrCodePermitDeny, "user permission deny")

	// 文章分类
	CateListFailed = renderx.NewRender(http.StatusOK, errCodeGetCateListFailed, "get category list failed")

	// 文章
	PostListFailed = renderx.NewRender(http.StatusOK, errCodeGetPostListFailed, "get post list failed")
)
