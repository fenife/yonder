package req

type GetPostListReq struct {
	CateId uint64 `form:"cate_id" binding:"omitempty,gte=1"` // 分类id
	Page   int    `form:"page" binding:"omitempty,gte=1"`
	Limit  int    `form:"limit" binding:"omitempty,gte=1"`
}

type GetPostDetailReq struct {
	PostId      uint64 `form:"post_id" binding:"required"`           // 文章id
	ContentType string `form:"ct" binding:"omitempty,oneof=html md"` // 文章内容类型，html或者markdown
}

type GetPostArchiveReq struct {
}

type GetPostAboutReq struct {
	ContentType string `form:"ct" binding:"omitempty,oneof=html md"`
}
