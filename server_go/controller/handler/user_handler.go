package handler

import (
	"github.com/gin-gonic/gin"
	"server-go/application"
	"server-go/controller/req"
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
// @Param        object body  req.CreateUserReq	false "查询参数"
// @Success      200  {object}  renderx.Response
// @Router       /api/v1/user/signup [post]
func (ctrl *UserHandler) UserSignup(c *gin.Context) {
	var userReq req.CreateUserReq
	if err := c.ShouldBindJSON(&userReq); err != nil {
		logx.Ctx(c).Errorf("param failed: %v", err)
		renderx.ErrOutput(c, errorx.ParamInvalid)
		return
	}

	_, err := ctrl.userApp.CreateUser(c, userReq.Name, userReq.Password)
	if err != nil {
		renderx.ErrOutput(c, err)
		return
	}
	renderx.SuccOutput(c)
}
