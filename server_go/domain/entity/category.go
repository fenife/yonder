package entity

type Category struct {
	BaseModel

	Name string `gorm:"type:varchar(255);not null;unique;comment:'分类名称'" json:"name"`
}
