package req

type GetPostListReq struct {
	CateId uint64 `form:"cate_id" binging:"omitempty,min=1"`
	Page   int    `form:"page" binging:"omitempty,min=1,default=1"`
	Limit  int    `form:"limit" binging:"omitempty,min=1,default=10"`
}

type GetPostDetailReq struct {
	PostId      uint64 `form:"post_id" binding:"required"`
	ContentType string `form:"ct" binding:"omitempty,oneof=html md"`
}

type GetPostArchiveReq struct {
}

type GetPostAboutReq struct {
	ContentType string `form:"content_type" binding:"omitempty,oneof=html md"`
}
