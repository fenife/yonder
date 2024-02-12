package req

type CreateUserReq struct {
	Name     string `json:"name" binding:"required"`
	Password string `json:"password" binding:"required"`
}
