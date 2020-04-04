package api

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/go-redis/redis/v7"
	"log"
	"strconv"
	yconf "yonder/config"
	"yonder/utils"
)

// for article list
type SimpleArticle struct {
	ID        uint           `json:"id"`
	CreatedAt utils.JSONTime `json:"created_at"`
	UpdatedAt utils.JSONTime `json:"updated_at"`
	Title     string         `json:"title"`
	UserId    uint           `json:"user_id"`
	UserName  string         `json:"user_name"`
	CateId    uint           `json:"cate_id"`
	CateName  string         `json:"cate_name"` // sql field: cate_name
}

func paginate(x []SimpleArticle, skip int, size int) []SimpleArticle {
	if skip > len(x) {
		skip = len(x)
	}

	end := skip + size
	if end > len(x) {
		end = len(x)
	}

	return x[skip:end]
}

// 根据标题搜索文章
func SearchArticle(c *gin.Context) {
	var err error
	var articles []SimpleArticle
	var page, limit int

	pageStr := c.Query("page")
	if pageStr == "" {
		// 不传page参数，默认为1
		page = 1
	} else if page, err = strconv.Atoi(pageStr); err != nil {
		log.Println(err)
		SendErrResp(c, "param `page` is not valid")
		return
	}

	limitStr := c.Query("limit")
	if limitStr == "" {
		limit = yconf.Conf.PageSize
	} else if limit, err = strconv.Atoi(limitStr); err != nil {
		log.Println(err)
		SendErrResp(c, "param `limit` is not valid")
		return
	}

	kw := c.Query("kw")
	if kw == "" {
		SendErrResp(c, "param `kw` is required")
		return
	}
	// add % to q
	fq := fmt.Sprintf("%%%s%%", kw)
	var sql = `
	select 
        a.id, a.title, a.created_at, a.updated_at, 
        a.user_id, b.name as user_name,
        a.cate_id, c.name as cate_name
    from articles a
    inner join users b on a.user_id = b.id
    inner join categories c on a.cate_id = c.id
    where a.status = 1 and b.status = 1 and c.status = 1
    and a.title like ?
    order by a.id desc`

	if err := utils.DB.Raw(sql, fq).Scan(&articles).Error; err != nil {
		log.Println(err)
		SendErrResp(c, "can not get article list")
		return
	}

	SendResp(c, gin.H{
		"articles":    paginate(articles, (page-1)*limit, limit),
		"total": len(articles),
	})
}

func Hello(c *gin.Context) {
	rds := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
	})
	v, _ := rds.Get("hello").Result()
	log.Println(v)
	c.JSON(200, gin.H{
		"value": v,
		"msg":   "hello world",
	})
}
