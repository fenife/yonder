package dto

import "server-go/domain/do"

type PostArchiveItem struct {
	Year     int              `json:"year"`
	Count    int              `json:"count"`
	PostList []*do.PostDetail `json:"post_list"`
}
