package req

type GetPostListReq struct {
	CateId uint64 `json:"cate_id" binding:"omitempty,gte=0"`
	Page   int    `json:"page" binding:"omitempty,gte=0,default=1"`
	Limit  int    `json:"limit" binding:"omitempty,gte=0,default=10"`
}
