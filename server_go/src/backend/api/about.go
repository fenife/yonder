package api

import (
	"log"

	"github.com/gin-gonic/gin"

	"backend/model"
	"backend/utils"
)

func About(c *gin.Context) {
	//var ac model.Article
	var err error
	var ad ArticleDetail

	err = model.DB.Where("title = 'about'").Find(&ad.Article).Error
	if err != nil {
		log.Println(err)
		SendErrResp(c, err.Error())
		return
	}

	// 作者
	err = model.DB.Where("id = ?", ad.Article.UserId).Find(&ad.User).Error
	if err != nil {
		log.Println(err)
		SendErrResp(c, err.Error())
		return
	}

	// 分类
	err = model.DB.Where("id = ?", ad.Article.CateId).Find(&ad.Category).Error
	if err != nil {
		log.Println(err)
		SendErrResp(c, err.Error())
		return
	}

	// content type
	ct := c.Query("ct")
	if ct == "html" {
		ad.Content = utils.MarkdownToHtml(ad.Content)
	}

	SendResp(c, gin.H{
		"ad": ad,
	})
}
