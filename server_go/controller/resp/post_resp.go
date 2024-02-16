package resp

import "server-go/application/dto"

type PostListResp struct {
	Total    int        `json:"total"`
	PostList []dto.Post `json:"post_list"`
}
