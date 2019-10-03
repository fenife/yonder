package api

import (
	"log"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"

	"backend/model"
)


// user register
func Signup(c *gin.Context)  {
	type UserSignupData struct {
		Name 		string 	`json:"name" binding:"required,min=4,max=20"`
		Password 	string 	`json:"password" binding:"required,min=3,max=20"`
	}

	var userInput UserSignupData
	if err := c.ShouldBindJSON(&userInput); err != nil {
		log.Println(err)
		SendErrResp(c, "输入有误，请检查")
		return
	}

	var validInput UserSignupData
	if err := Deepcopy(&userInput, &validInput); err != nil {
		SendErrResp(c, "内部错误")
		return
	}

	validInput.Name = model.PreventXSS(userInput.Name)
	validInput.Name = strings.TrimSpace(userInput.Name)
	if validInput.Name != userInput.Name {
		SendErrResp(c, "名称中包含空格")
		return
	}

	var user model.User
	err := model.DB.Where("name = ?", validInput.Name).Find(&user).Error
	if err == nil {
		// 说明该用户名已经存在
		if user.Name == validInput.Name {
			SendErrResp(c, "username {" + user.Name + "} has been existed.")
			return
		}
	}

	var newUser model.User
	newUser.Name = validInput.Name
	newUser.Passwd = newUser.EncryptPasswd(validInput.Password)
	newUser.Role = model.UserRoleNormal
	newUser.Status = model.UserStatusActive

	if err := model.DB.Create(&newUser).Error; err != nil {
		log.Print(err)
		SendErrResp(c, "can not create user")
		return
	}

	SendResp(c, gin.H{
		"user": newUser,
	})
}

// user login in
func Login(c *gin.Context)  {
	// todo: 避免多次重复登陆

	type UserLogin struct {
		Name 		string 	`json:"name" binding:"required,min=4,max=20"`
		Password 	string 	`json:"password" binding:"required,min=3,max=20"`
	}

	var userInput UserLogin
	if err := c.ShouldBindJSON(&userInput); err != nil {
		log.Println(err)
		SendErrResp(c, "输入有误，请检查")
		return
	}

	var user model.User
	err := model.DB.Where("name = ?", userInput.Name).Find(&user).Error
	if err != nil {
		SendErrResp(c, "user not found")
		return
	}

	// 检查密码是否错误
	if !user.CheckPasswd(userInput.Password) {
		SendErrResp(c, "password is not correct")
		return
	}

	// 检查用户是否已删除
	if user.Status != model.UserStatusActive {
		SendErrResp(c, "user not found")
		return
	}

	// 设置 cookie token
	token, err := user.GetSessionToken()
	if err != nil {
		log.Println(err)
		SendErrResp(c, "internal err")
		return
	}

	if err := model.SaveTokenToRedis(token, user.ID); err != nil {
		log.Println(err)
		SendErrResp(c, "internal err")
		return
	}

	if err := model.SaveUserToRedis(user); err != nil {
		log.Println(err)
		SendErrResp(c, "internal err")
		return
	}

	// todo: max age of config
	maxAge := 60 * 60 * 24
	c.SetCookie("token", token, maxAge, "/", "", true, true)

	SendResp(c, gin.H{
		"token": token,
		"user": user,
	})
}

func ResetPasswd(c *gin.Context) {
	// todo: not done yet
	userInfo, _ := c.Get("user")
	user := userInfo.(model.User)

	SendResp(c, gin.H{
		"user": user,
	})
}


func UserList(c *gin.Context) {
	var users []model.User
	if err := model.DB.Order("id asc").Find(&users).Error; err != nil {
		msg := "can not get user list"
		SendErrResp(c, msg)
		log.Print(msg, err.Error)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"errNo": ErrCode.SUCCESS,
		"msg": "success",
		"data": gin.H{
			"users": users,
		},
	})
}

func UserInfo(c *gin.Context) {
	var user model.User
	if userInfo, ok := c.Get("user"); ok {
		user = userInfo.(model.User)
		SendResp(c, gin.H{
			"user": user,
		})
	}
}

func SignOut(c *gin.Context) {
	if userInfo, ok := c.Get("user"); ok {
		user := userInfo.(model.User)
		if err := model.RemoveUserFromRedis(user); err != nil {
			SendErrResp(c, "sign out error")
		}

		SendResp(c, gin.H{})
	}
}
