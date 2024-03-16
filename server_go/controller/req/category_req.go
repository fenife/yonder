package req

type CreateCategoryReq struct {
	Name string `json:"name" binding:"required"` // 分类名称
}
