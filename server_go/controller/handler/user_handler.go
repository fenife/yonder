package handler

import (
	"github.com/gin-gonic/gin"
	"server-go/application"
	"server-go/controller/req"
	"server-go/controller/resp"
	"server-go/internal/errorx"
	"server-go/pkg/logx"
	"server-go/pkg/renderx"
)

type UserHandler struct {
	userApp application.IUserApp
}

func NewUserHandler(userApp application.IUserApp) *UserHandler {
	return &UserHandler{
		userApp: userApp,
	}
}

// UserSignup godoc
// @Summary      用户注册
// @Description  创建新用户
// @Tags         users
// @Accept       json
// @Produce      json
// @Param        object body  req.SignupReq	false "查询参数"
// @Success      200  {object}  renderx.Response
// @Router       /api/v1/user/signup [post]
func (ctrl *UserHandler) UserSignup(c *gin.Context) {
	var userReq req.SignupReq
	if err := c.ShouldBindJSON(&userReq); err != nil {
		logx.Ctx(c).With("error", err).Errorf("param error")
		renderx.ErrOutput(c, errorx.ParamInvalid)
		return
	}

	_, err := ctrl.userApp.Signup(c, userReq.Name, userReq.Password)
	if err != nil {
		if _, ok := err.(*renderx.Render); !ok {
			logx.Ctx(c).With("error", err).Errorf("create user failed")
			err = errorx.UserSignupFailed
		}
		renderx.ErrOutput(c, err)
		return
	}
	renderx.SuccOutput(c)
}

// UserSignIn godoc
// @Summary      用户登陆
// @Description	 检查用户是否存在，密码是否正确，如果正常，返回用户token
// @Tags         users
// @Accept       json
// @Produce      json
// @Param        object body  req.SignInReq	false "查询参数"
// @Success      200  {object}  resp.SignInResp
// @Failure      2101  integer 	"其他原因导致的登陆失败"
// @Failure      2102  integer 	"用户不存在"
// @Failure      2103  integer 	"用户名或密码不正确"
// @Failure      2104  integer 	"用户已登陆"
// @Router       /api/v1/user/signin [post]
func (ctrl *UserHandler) UserSignIn(c *gin.Context) {
	var userReq req.SignInReq
	if err := c.ShouldBindJSON(&userReq); err != nil {
		logx.Ctx(c).With("error", err).Errorf("param error")
		renderx.ErrOutput(c, errorx.ParamInvalid)
		return
	}

	user, token, err := ctrl.userApp.SignIn(c, userReq.Name, userReq.Password)
	if err != nil {
		if _, ok := err.(*renderx.Render); !ok {
			logx.Ctx(c).With("error", err).Errorf("user sign in failed")
			err = errorx.UserSignupFailed
		}
		renderx.ErrOutput(c, err)
		return
	}

	data := resp.SignInResp{
		UserName:  user.Name,
		UserToken: token,
	}
	renderx.SuccOutput(c, data)
}
