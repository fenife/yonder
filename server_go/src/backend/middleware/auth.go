package middleware

import (
	"errors"
	"log"

	"github.com/gin-gonic/gin"

	"backend/api"
	"backend/config"
	"backend/model"
)

// 根据请求中的token从redis中获取用户信息
func getUser(c *gin.Context) (model.User, error)  {
	var user model.User
	//token := c.GetHeader("token")
	token, err := c.Cookie("token")
	if err != nil {
		log.Println("token err")
		return user, errors.New("token err")
	}

	userId, err := model.GetUserIdByToken(token)
	if err != nil {
		log.Println(err)
		return user, err
	}

	user, err = model.GetUserFromRedis(userId)
	if err != nil {
		log.Println(err)
		return user, err
	}
	
	return user, nil
}

// 部分数据必须登陆才能查看
func LoginRequired(c *gin.Context) {
	// todo: 后续可以通过 jwt 验证
	user, err := getUser(c)
	if err != nil {
		api.SendErrResp(c, "not login")
		return
	}

	c.Set("user", user)
	c.Next()
}

// 必须是管理员权限
func AdminRequired(c *gin.Context) {
	user, err := getUser(c)
	if err != nil {
		api.SendErrResp(c, "not login")
		return
	}

	adminName := config.AllConfig.Admin.Name
	if !(user.Role == model.UserRoleAdmin && user.Name == adminName) {
		api.SendErrResp(c, "permission denied")
		return
	}

	c.Set("user", user)
	c.Set("admin", user)
	c.Next()
}

func isAdmin(c *gin.Context) bool {
	val, ok := c.Get("user")
	if !ok {
		return false
	}

	adminName := config.AllConfig.Admin.Name
	user := val.(model.User)
	if user.Role == model.UserRoleAdmin && user.Name == adminName {
		return true
	}

	return false
}
