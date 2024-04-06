package req

type CreateCategoryReq struct {
	Name string `json:"name" binding:"required"` // 分类名称
}

type UpdateCategoryReq struct {
	Id   uint64 `json:"id" binding:"required"`   // 分类id
	Name string `json:"name" binding:"required"` // 分类名称
}
