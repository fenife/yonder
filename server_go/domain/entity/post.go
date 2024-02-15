package entity

type Post struct {
	BaseModel

	UserId  uint64 `gorm:"type:bigint;index;not null;comment:'用户id'" json:"user_id"`
	CateId  uint64 `gorm:"type:bigint;index;not null;comment:'分类id'" json:"cate_id"`
	Title   string `gorm:"type:varchar(255);not null;unique;comment:'中文标题'" json:"title"`
	TitleEn string `gorm:"type:varchar(255);not null;unique;comment:'英文标题'" json:"title_en"`
	Content string `gorm:"type:text;not null;comment:'文章内容'" json:"content"`
}
