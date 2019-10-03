package api

import (
	"errors"
	"fmt"
	"log"
	"strconv"
	//"time"

	"github.com/gin-gonic/gin"

	"backend/config"
	"backend/model"
	"backend/utils"
)

type Pagination struct {
	Total int
}

// for article list
type SimpleArticle struct {
	ID        uint
	CreatedAt utils.JSONTime
	UpdatedAt utils.JSONTime
	Title 	  string
	UserId 	  uint
	Username  string		// sql field: username
	CateId 	  uint			// sql field: cate_id
	CateName  string 		// sql field: cate_name
}

// for article retrieve
type ArticleDetail struct {
	model.Article
	User model.User
	Category model.Category
}

type TinyArticle struct {
	ID        uint
	CreatedAt utils.JSONTime
	UpdatedAt utils.JSONTime
	Title 	  string
}

func getArticleDetail(id uint) (ArticleDetail, error) {
	var err error
	var ad ArticleDetail
	//sql := ``

	return ad, err
}

func GetArticleDetail(id uint) (ArticleDetail, error) {
	//var ac model.Article
	var err error
	var ad ArticleDetail

	err = model.DB.Where("id = ?", id).Find(&ad.Article).Error
	if err != nil {
		log.Println(err)
		return ad, errors.New("article not existed")
	}

	// 作者
	err = model.DB.Where("id = ?", ad.Article.UserId).Find(&ad.User).Error
	if err != nil {
		log.Println(err)
		return ad, errors.New("article author not existed")
	}

	// 分类
	err = model.DB.Where("id = ?", ad.Article.CateId).Find(&ad.Category).Error
	if err != nil {
		log.Println(err)
		return ad, errors.New("article category not existed")
	}

	return ad, nil
}

func ArticleList(c *gin.Context)  {
	// todo: page and limit
	// todo: filter by cateId

	var cateId int
	var err error
	var al []SimpleArticle
	var page, limit int
	//var total uint
	var pagination Pagination

	cateIdStr := c.Query("cateId")
	if cateIdStr == "" {
		cateId = 0
	} else if cateId, err = strconv.Atoi(cateIdStr); err != nil {
		log.Println(err)
		SendErrResp(c, "cate id is not valid")
		return
	}

	pageStr := c.Query("page")
	if pageStr == "" {
		// 不传page参数，默认为1
		page = 1
	} else if page, err = strconv.Atoi(pageStr); err != nil {
		log.Println(err)
		SendErrResp(c, "param page no is not valid")
		return
	}

	limitStr := c.Query("limit")
	if limitStr == "" {
		limit = config.AllConfig.Page.Size
	} else if limit, err = strconv.Atoi(limitStr); err != nil {
		log.Println(err)
		SendErrResp(c, "param limit is not valid")
		return
	}

	var cate model.Category
	if cateId != 0 && model.DB.First(&cate, cateId).Error != nil {
		SendErrResp(c, "cate id is not valid")
		return
	}

	// 可展示的文章总数
	// import !!! 必须要用别名 total，否则gorm对结果无法解析
	var totalSql = `
	SELECT count(1) as total
	FROM articles a 
	INNER JOIN users b ON a.user_id = b.id 
	INNER JOIN categories c ON a.cate_id = c.id
	WHERE a.deleted_at IS NULL AND b.deleted_at IS NULL AND c.deleted_at IS NULL`

	var sql = `
	SELECT a.id, a.title, a.created_at, a.updated_at, a.user_id, b.name as username, 
	a.cate_id, c.name as cate_name
	FROM articles a 
	INNER JOIN users b ON a.user_id = b.id 
	INNER JOIN categories c ON a.cate_id = c.id
	WHERE a.deleted_at IS NULL AND b.deleted_at IS NULL AND c.deleted_at IS NULL `

	if cateId != 0 {
		extra := fmt.Sprintf(` AND c.id = %d`, cateId)
		totalSql += extra
		sql += extra
	} else {
		extra := fmt.Sprintf(` ORDER BY a.updated_at DESC`)
		sql += extra
	}

	if err := model.DB.Raw(totalSql).First(&pagination).Error; err != nil {
		log.Println(err)
		SendErrResp(c, "can not get article counts")
		return
	}

	// 限制数目
	sql += fmt.Sprintf(" LIMIT %d, %d", (page - 1) * limit, limit)

	if err := model.DB.Raw(sql).Scan(&al).Error; err != nil {
		log.Println(err)
		SendErrResp(c, "can not get article list")
		return
	}

	SendResp(c, gin.H{
		"al": al,
		"total": pagination.Total,
	})
}

func ArticleRetrieve(c *gin.Context)  {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		log.Println(err)
		SendErrResp(c, "invalid article id")
		return
	}

	ad, err := GetArticleDetail(uint(id))
	if err != nil {
		SendErrResp(c, err.Error())
		return
	}

	// content type
	ct := c.Query("ct")
	if ct == "html" {
		ad.Content = utils.MarkdownToHtml(ad.Content)
	}

	// get pre article
	pre, err := ad.GetPre()
	if err != nil {
		log.Println(err)
		pre = nil
	}

	// get next article
	next, err := ad.GetNext()
	if err != nil {
		log.Println(err)
		next = nil
	}

	SendResp(c, gin.H{
		"ad": ad,
		"pre": pre,
		"next": next,
	})
}

func ArticleCreate(c *gin.Context)  {
	val, _ := c.Get("user")		// interface{}
	user := val.(model.User)

	var ac model.Article
	if err := c.ShouldBindJSON(&ac); err != nil {
		log.Println(err)
		SendErrResp(c, "输入有误，请检查")
		return
	}
	ac.UserId = user.ID

	if err := ac.Create(); err != nil {
		SendErrResp(c, err.Error())
		return
	}

	//SendResp(c, gin.H{})
	ad, err := GetArticleDetail(ac.ID)
	if err != nil {
		SendErrResp(c, err.Error())
		return
	}

	SendResp(c, gin.H{
		"ad": ad,
	})
}

func ArticleUpdate(c *gin.Context)  {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		log.Println(err)
		SendErrResp(c, "invalid article id")
		return
	}

	val, _ := c.Get("user")		// interface{}
	user := val.(model.User)

	var ac model.Article
	if err := c.ShouldBindJSON(&ac); err != nil {
		log.Println(err)
		SendErrResp(c, "输入有误，请检查")
		return
	}
	ac.UserId = user.ID

	if err := ac.Update(id); err != nil {
		SendErrResp(c, err.Error())
		return
	}

	// todo: 获取文章详情，是否可以优化
	//ArticleRetrieve(c)
	ad, err := GetArticleDetail(uint(id))
	if err != nil {
		SendErrResp(c, err.Error())
		return
	}

	SendResp(c, gin.H{
		"ad": ad,
	})
}

func ArticleDestroy(c *gin.Context)  {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		log.Println(err)
		SendErrResp(c, "invalid article id")
		return
	}

	var ac model.Article
	err = model.DB.First(&ac, "id = ?", id).Error
	if err != nil {
		log.Println(err)
		SendErrResp(c, "article not existed")
		return
	}

	if err := model.DB.Delete(&ac).Error; err != nil {
		log.Println(err)
		SendErrResp(c, "delete article error")
		return
	}

	SendResp(c, gin.H{})
}
