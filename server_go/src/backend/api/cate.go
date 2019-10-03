package api

import (
	"log"
	"strconv"

	"github.com/gin-gonic/gin"

	"backend/model"
)

type ArticleCount struct {
	CateId uint	// category id
	Count uint	// 该分类下的可见文章总数
}

type CateWithCount struct {
	model.Category
	Count uint		// 该分类下的可见文章总数
}

func CateList(c *gin.Context)  {
	// todo: add page and limit
	var cateList []CateWithCount
	var results []ArticleCount
	acMap := make(map[uint]uint)
	if err := model.DB.Table("categories").Find(&cateList).Error; err != nil {
		log.Println(err)
		SendErrResp(c, err.Error())
		return
	}

	err := model.DB.Table("articles").Select("cate_id, count(*) as count").Where(
		"deleted_at IS NULL").Group(
		"cate_id").Scan(&results).Error
	if err != nil {
		log.Println(err)
		SendErrResp(c, "can not count articles")
		return
	}
	// array to map
	for _, v := range results {
		acMap[v.CateId] = v.Count
	}

	// set article counts of each category
	for i, c := range cateList {
		cnt, ok := acMap[c.ID]
		if !ok {
			cateList[i].Count = 0
		}
		cateList[i].Count = cnt
	}

	SendResp(c, gin.H{
		"cateList": cateList,
	})
}

func CateRetrieve(c *gin.Context)  {
	cateId, err := strconv.Atoi(c.Param("cateId"))
	if err != nil {
		log.Println(err)
		SendErrResp(c, "invalid category id")
		return
	}

	var cate model.Category
	err = model.DB.Where("id = ?", cateId).Find(&cate).Error
	if err != nil {
		log.Println(err)
		SendErrResp(c, "category not existed")
		return
	}

	SendResp(c, gin.H{
		"cate": cate,
	})
}

func CateCreate(c *gin.Context)  {
	var cate model.Category
	if err := c.ShouldBindJSON(&cate); err != nil {
		log.Println(err)
		SendErrResp(c, "输入有误，请检查")
		return
	}

	if err := cate.Create(); err != nil {
		SendErrResp(c, err.Error())
		return
	}

	SendResp(c, gin.H{
		"cate": cate,
	})
}

func CateUpdate(c *gin.Context)  {
	cateId, err := strconv.Atoi(c.Param("cateId"))
	if err != nil {
		log.Println(err)
		SendErrResp(c, "invalid category id")
		return
	}

	var cate model.Category
	if err := c.ShouldBindJSON(&cate); err != nil {
		log.Println(err)
		SendErrResp(c, "输入有误，请检查")
		return
	}

	if err := cate.Update(cateId); err != nil {
		SendErrResp(c, err.Error())
		return
	}

	SendResp(c, gin.H{
		"cate": cate,
	})

}

func CateDestroy(c *gin.Context)  {
	// todo: 该分类下的文章是否还可见？
	cateId, err := strconv.Atoi(c.Param("cateId"))
	if err != nil {
		log.Println(err)
		SendErrResp(c, "invalid category id")
		return
	}

	var cate model.Category
	err = model.DB.First(&cate, "id = ?", cateId).Error
	if err != nil {
		log.Println(err)
		SendErrResp(c, "category not existed")
		return
	}

	if err := model.DB.Delete(&cate).Error; err != nil {
		log.Println(err)
		SendErrResp(c, "delete category error")
		return
	}

	SendResp(c, gin.H{})
}
