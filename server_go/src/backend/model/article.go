package model

import (
	"errors"
	"log"
)

type Article struct {
	//gorm.Model
	BaseModel
	UserId uint `gorm:"not null;index"`
	//User   User
	CateId 		uint 	`gorm:"not null;index" binding:"required"`
	//Category 	Category
	Title 		string `gorm:"not null;index" binding:"required"`
	Content   string 	`gorm:"type:text;not null" binding:"required"`
}

func (ac *Article) checkInput() error {
	ac.Title = PreventXSS(ac.Title)
	//ac.Content = PreventXSS(ac.Content)

	// 检查分类是否存在
	if err := IsCateExisted(ac.CateId); err != nil{
		return err
	}

	return nil
}

func (ac *Article) Create() error {
	if err := ac.checkInput(); err != nil {
		return err
	}

	// 同标题的文章是否存在
	err := DB.Select("id").Where("title = ?", ac.Title).Find(&ac).Error
	if err == nil {
		//说明该标题已经存在
		return errors.New("article has been existed")
	}

	if err := DB.Create(ac).Error; err != nil {
		log.Println(err)
		return errors.New("create article error")
	}

	return nil
}

func (ac *Article) Update(id int) error {
	if err := ac.checkInput(); err != nil {
		return err
	}

	// 除了其自身外，同标题的文章是否存在
	err := DB.Select("id").Where("id != ? and title = ?", id, ac.Title).Find(&ac).Error
	if err == nil {
		//说明该标题已经存在
		return errors.New("article has been existed")
	}

	// todo: 可优化，只有url中传进来的字段才更新
	// 目前要求文章的所有字段都要传进来
	upd := make(map[string]interface{})
	upd["title"] = ac.Title
	upd["cateId"] = ac.CateId
	upd["content"] = ac.Content
	//upd["userId"] = ac.UserId

	if err := DB.Where("id = ?", id).First(&ac).Error; err != nil {
		log.Println(err)
		return errors.New("article not existed")
	}

	if err := DB.Model(&ac).Updates(upd).Error; err != nil {
		log.Println(err)
		return errors.New("update article error")
	}

	return nil
}

func (ac *Article) GetPre() (*Article, error) {
	var pre Article

	err := DB.Select("id, title").Where("id < ?", ac.ID).Last(&pre).Error
	return &pre, err
}

func (ac *Article) GetNext() (*Article, error) {
	var next Article

	err := DB.Select("id, title").Where("id > ?", ac.ID).First(&next).Error
	return &next, err
}
