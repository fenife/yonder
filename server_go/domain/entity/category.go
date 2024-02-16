package entity

type Category struct {
	BaseModel

	Name string `gorm:"type:varchar(255);not null;unique;comment:'分类名称'" json:"name"`
}

func (u *Category) IsValid() bool {
	// 未删除，且id>0
	return u.DeletedAt.Valid == false && u.ID > 0
}
