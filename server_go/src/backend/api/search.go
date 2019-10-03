package api

import (
	"fmt"
	"log"
	"strconv"

	"github.com/gin-gonic/gin"

	"backend/config"
	"backend/model"
)

func paginate(x []SimpleArticle, skip int, size int) []SimpleArticle {
	if skip > len(x) {
		skip = len(x)
	}

	end := skip + size
	if end > len(x) {
		end = len(x)
	}

	return x[skip: end]
}

func SearchArticle(c *gin.Context)  {
	var err error
	var al []SimpleArticle
	var page, limit int

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

	q := c.Query("q")
	// add % to q
	fq := fmt.Sprintf("%%%s%%", q)
	var sql = `
	SELECT a.id, a.title, a.created_at, a.updated_at, a.user_id, b.name as username, 
	a.cate_id, c.name as cate_name
	FROM articles a 
	INNER JOIN users b ON a.user_id = b.id 
	INNER JOIN categories c ON a.cate_id = c.id
	WHERE a.deleted_at IS NULL AND b.deleted_at IS NULL AND c.deleted_at IS NULL
	AND a.title like ?`

	if err := model.DB.Raw(sql, fq).Scan(&al).Error; err != nil {
		log.Println(err)
		SendErrResp(c, "can not get article list")
		return
	}

	SendResp(c, gin.H{
		"al": paginate(al, (page - 1) * limit, limit),
		"total": len(al),
	})
}
