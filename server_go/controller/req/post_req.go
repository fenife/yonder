package req

type GetPostListReq struct {
	CateId uint64 `form:"cate_id" binging:"omitempty,min=1"`
	Page   int    `form:"page" binging:"omitempty,min=1,default=1"`
	Limit  int    `form:"limit" binging:"omitempty,min=1,default=10"`
}
