package handler

import (
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
	"server-go/application"
	"server-go/domain/entity"
)

type UserHandler struct {
	ua application.IUserApp
}

func NewUserHandler(ua application.IUserApp) *UserHandler {
	return &UserHandler{
		ua: ua,
	}
}

type CreateUserReq struct {
	Name     string `json:"name" binding:"required"`
	Password string `json:"password" binding:"required"`
}

func (ctrl *UserHandler) CreateUser(c *gin.Context) {
	var userReq CreateUserReq
	if err := c.ShouldBindJSON(&userReq); err != nil {
		log.Println("err:", err)
		c.JSON(http.StatusUnprocessableEntity, gin.H{
			"invalid_json": "invalid json",
		})
		return
	}

	user := entity.User{
		Name:     userReq.Name,
		Password: userReq.Password,
		Status:   1,
	}

	newUser, err := ctrl.ua.CreateUser(c, &user)
	if err != nil {
		c.JSON(http.StatusInternalServerError, err)
		return
	}
	c.JSON(http.StatusOK, newUser)
}
