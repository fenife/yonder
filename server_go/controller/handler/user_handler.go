package handler

import (
	"github.com/gin-gonic/gin"
	"server-go/application"
	"server-go/controller/req"
	"server-go/domain/entity"
	"server-go/internal/errorx"
	"server-go/utils/logx"
	"server-go/utils/renderx"
)

type UserHandler struct {
	ua application.IUserApp
}

func NewUserHandler(ua application.IUserApp) *UserHandler {
	return &UserHandler{
		ua: ua,
	}
}

// CreateUser godoc
// @Summary      创建用户
// @Description  新用户注册
// @Tags         users
// @Accept       json
// @Produce      json
// @Param        object body  req.CreateUserReq	false "查询参数"
// @Success      200  {object}  renderx.Response
// @Router       /user [post]
func (ctrl *UserHandler) CreateUser(c *gin.Context) {
	var userReq req.CreateUserReq
	if err := c.ShouldBindJSON(&userReq); err != nil {
		logx.Ctx(c).Errorf("param failed: %v", err)
		renderx.ErrOutput(c, errorx.ParamInvalid)
		return
	}

	user := entity.User{
		Name:     userReq.Name,
		Password: userReq.Password,
		Status:   1,
	}

	newUser, err := ctrl.ua.CreateUser(c, &user)
	if err != nil {
		renderx.ErrOutput(c, err)
		return
	}
	renderx.SuccOutput(c, newUser)
}
