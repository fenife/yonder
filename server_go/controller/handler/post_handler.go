package handler

import (
	"github.com/gin-gonic/gin"
	"server-go/application/aservice"
	"server-go/controller/req"
	"server-go/controller/resp"
	"server-go/internal/errorx"
	"server-go/pkg/logx"
	"server-go/pkg/renderx"
)

type PostHandler struct {
	postApp aservice.IPostApp
}

func NewPostHandler(postApp aservice.IPostApp) *PostHandler {
	return &PostHandler{
		postApp: postApp,
	}
}

// GetPostList godoc
// @Summary      文章列表
// @Description	 获取文章列表，支持分页，可按分类id进行查询
// @Tags         post
// @Accept       json
// @Produce      json
// @Param        object body  req.GetPostListReq	false "查询参数"
// @Success      200  {object}  resp.PostListResp
// @Router       /api/v1/post/list [get]
func (ctrl *PostHandler) GetPostList(c *gin.Context) {
	var postReq req.GetPostListReq
	if err := c.ShouldBindQuery(&postReq); err != nil {
		logx.Ctx(c).With("error", err).Errorf("param error")
		renderx.ErrOutput(c, errorx.ParamInvalid)
		return
	}

	posts, err := ctrl.postApp.GetPostList(c, postReq.CateId, postReq.Page, postReq.Limit)
	if err != nil {
		logx.Ctx(c).With("error", err).Errorf("get posts failed")
		renderx.ErrOutput(c, err)
		return
	}

	result := resp.PostListResp{
		Total:    len(posts),
		PostList: posts,
	}
	renderx.SuccOutput(c, result)
}
