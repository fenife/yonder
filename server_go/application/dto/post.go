package dto

import "server-go/domain/do"

type PostBrief struct {
	ID        uint64 `json:"id"`
	CreatedAt string `json:"created_at"` // "2006-01-02 15:05:05"
	UpdatedAt string `json:"updated_at"` // 同上
	UserId    uint64 `json:"user_id"`
	CateId    uint64 `json:"cate_id"`
	Title     string `json:"title"`
	TitleEn   string `json:"title_en"`
}

type PostDetail struct {
	PostBrief
	Content  string           `json:"content"` // 文章详情
	User     *do.UserTiny     `json:"user"`
	Category *do.CategoryTiny `json:"category"`
}

type PostArchiveItem struct {
	Year     int           `json:"year"`
	Count    int           `json:"count"`
	PostList []*PostDetail `json:"post_list"`
}
