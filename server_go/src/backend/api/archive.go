package api

import (
	"backend/model"
	"backend/utils"
	"github.com/gin-gonic/gin"
	"log"
	"sort"
)

type SmallArticle struct {
	ID        uint
	CreatedAt utils.JSONTime
	UpdatedAt utils.JSONTime
	Title 	  string
}

// 某一年的所有可见文章
type ArticleArchive struct {
	Year 	int
	ArtList []SmallArticle
	Count 	int
}

func (box *ArticleArchive) AddItem(item SmallArticle) []SmallArticle {
	box.ArtList = append(box.ArtList, item)
	return box.ArtList
}

func (box *ArticleArchive) ItemLen() int {
	return len(box.ArtList)
}

type ArchiveSlice []ArticleArchive

func (sl ArchiveSlice) Len() int           { return len(sl)}
func (sl ArchiveSlice) Less(i, j int) bool { return sl[i].Year < sl[j].Year}
func (sl ArchiveSlice) Swap(i, j int)      { sl[i], sl[j] = sl[j], sl[i] }

func oldArchive(c *gin.Context)  {
	var arList []SmallArticle

	// 可展示的文章总数
	// import !!! 必须要用别名 total，否则gorm对结果无法解析
	var sql = `
	SELECT a.id, a.title, a.created_at, a.updated_at
	FROM articles a 
	INNER JOIN users b ON a.user_id = b.id 
	INNER JOIN categories c ON a.cate_id = c.id
	WHERE a.deleted_at IS NULL AND b.deleted_at IS NULL AND c.deleted_at IS NULL`

	if err := model.DB.Raw(sql).Scan(&arList).Error; err != nil {
		log.Println(err)
		SendErrResp(c, "can not get article list")
		return
	}

	alMap := make(map[int]ArticleArchive)

	for _, a := range arList {
		year := a.CreatedAt.Year()
		_, ok := alMap[year]
		if !ok {
			alMap[year] = ArticleArchive{ArtList: []SmallArticle{}, Count: 0}
		}
		yearArts, _ := alMap[year]
		yearArts.AddItem(a)
		alMap[year] = yearArts
	}

	for year, arts := range alMap {
		arts.Count = len(arts.ArtList)
		alMap[year] = arts
	}

	SendResp(c, gin.H{
		"al": alMap,
	})
}

func Archive(c *gin.Context) {
	var arList []SmallArticle
	var yearLine ArchiveSlice

	// 可展示的文章总数
	// import !!! 必须要用别名 total，否则gorm对结果无法解析
	var sql = `
	SELECT a.id, a.title, a.created_at, a.updated_at
	FROM articles a 
	INNER JOIN users b ON a.user_id = b.id 
	INNER JOIN categories c ON a.cate_id = c.id
	WHERE a.deleted_at IS NULL AND b.deleted_at IS NULL AND c.deleted_at IS NULL
	ORDER BY a.created_at DESC`

	if err := model.DB.Raw(sql).Scan(&arList).Error; err != nil {
		log.Println(err)
		SendErrResp(c, "can not get article list")
		return
	}

	alMap := make(map[int]ArticleArchive)

	for _, a := range arList {
		year := a.CreatedAt.Year()
		_, ok := alMap[year]
		if !ok {
			alMap[year] = ArticleArchive{Year: year, ArtList: []SmallArticle{}, Count: 0}
		}
		yearArts, _ := alMap[year]
		yearArts.AddItem(a)
		alMap[year] = yearArts
	}

	for year, arts := range alMap {
		arts.Count = len(arts.ArtList)
		alMap[year] = arts
		yearLine = append(yearLine, arts)
	}

	sort.Sort(sort.Reverse(yearLine))

	SendResp(c, gin.H{
		"al": yearLine,
	})
}
