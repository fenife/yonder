package dto

import "time"

type Post struct {
	ID        uint64    `json:"id"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
	UserId    uint64    `json:"user_id"`
	CateId    uint64    `json:"cate_id"`
	Title     string    `json:"title"`
	TitleEn   string    `json:"title_en"`
	Content   string    `json:"content"`
}
