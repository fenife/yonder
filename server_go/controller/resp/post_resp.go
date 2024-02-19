package resp

import (
	"server-go/application/dto"
	"server-go/domain/do"
)

type PostListResp struct {
	Total    int             `json:"total"`
	PostList []*do.PostSmall `json:"post_list"`
}

type PostDetailResp struct {
	do.PostDetail
}

type PostArchiveResp struct {
	List []*dto.PostArchiveItem `json:"list"`
}
