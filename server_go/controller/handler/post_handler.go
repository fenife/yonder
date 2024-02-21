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
// @Param        object query  req.GetPostListReq	false "查询参数"
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

// GetPostDetail godoc
// @Summary      文章详情
// @Description	 获取文章详情，包括用户和分类信息
// @Tags         post
// @Accept       json
// @Produce      json
// @Param        object query  req.GetPostDetailReq	false "查询参数"
// @Success      200  {object}  resp.PostDetailResp
// @Router       /api/v1/post/detail [get]
func (ctrl *PostHandler) GetPostDetail(c *gin.Context) {
	var postReq req.GetPostDetailReq
	if err := c.ShouldBindQuery(&postReq); err != nil {
		logx.Ctx(c).With("error", err).Errorf("param error")
		renderx.ErrOutput(c, errorx.ParamInvalid)
		return
	}

	detail, err := ctrl.postApp.GetPostDetail(c, postReq.PostId, postReq.ContentType)
	if err != nil {
		logx.Ctx(c).With("error", err).Errorf("get posts failed")
		renderx.ErrOutput(c, err)
		return
	}

	renderx.SuccOutput(c, detail)
}

// GetPostArchive godoc
// @Summary      文章归档列表
// @Description	 获取文章归档列表，包括用户和分类信息
// @Tags         post
// @Accept       json
// @Produce      json
// @Param        object query  req.GetPostArchiveReq	false "查询参数"
// @Success      200  {object}  resp.PostArchiveResp
// @Router       /api/v1/post/archive [get]
func (ctrl *PostHandler) GetPostArchive(c *gin.Context) {
	//var postReq req.GetPostArchiveReq
	//if err := c.ShouldBindQuery(&postReq); err != nil {
	//	logx.Ctx(c).With("error", err).Errorf("param error")
	//	renderx.ErrOutput(c, errorx.ParamInvalid)
	//	return
	//}

	postList, err := ctrl.postApp.GetPostArchiveList(c)
	if err != nil {
		logx.Ctx(c).With("error", err).Errorf("get posts failed")
		renderx.ErrOutput(c, err)
		return
	}
	result := resp.PostArchiveResp{
		List: postList,
	}
	renderx.SuccOutput(c, result)
}

// GetPostAbout godoc
// @Summary      about文章内容
// @Description	 获取about文章详情，用于about页面展示
// @Tags         post
// @Accept       json
// @Produce      json
// @Param        object query  req.GetPostAboutReq	false "查询参数"
// @Success      200  {object}  resp.PostDetailResp
// @Router       /api/v1/post/about [get]
func (ctrl *PostHandler) GetPostAbout(c *gin.Context) {
	var postReq req.GetPostAboutReq
	if err := c.ShouldBindQuery(&postReq); err != nil {
		logx.Ctx(c).With("error", err).Errorf("param error")
		renderx.ErrOutput(c, errorx.ParamInvalid)
		return
	}

	detail, err := ctrl.postApp.GetPostAbout(c, postReq.ContentType)
	if err != nil {
		logx.Ctx(c).With("error", err).Errorf("get posts failed")
		renderx.ErrOutput(c, err)
		return
	}

	renderx.SuccOutput(c, detail)
}

// SearchPostByTitle godoc
// @Summary      文章搜索
// @Description	 根据标题搜索文章列表
// @Tags         post
// @Accept       json
// @Produce      json
// @Param        object query  req.SearchPostReq	false "查询参数"
// @Success      200  {object}  resp.PostListResp
// @Router       /api/v1/post/search [get]
func (ctrl *PostHandler) SearchPostByTitle(c *gin.Context) {
	var postReq req.SearchPostReq
	if err := c.ShouldBindQuery(&postReq); err != nil {
		logx.Ctx(c).With("error", err).Errorf("param error")
		renderx.ErrOutput(c, errorx.ParamInvalid)
		return
	}

	postDetails, err := ctrl.postApp.SearchPostByTitle(c, postReq.KeyWord, postReq.Page, postReq.Limit)
	if err != nil {
		logx.Ctx(c).With("error", err).Errorf("get posts failed")
		renderx.ErrOutput(c, err)
		return
	}
	result := resp.PostListResp{
		Total:    len(postDetails),
		PostList: postDetails,
	}
	renderx.SuccOutput(c, result)
}
