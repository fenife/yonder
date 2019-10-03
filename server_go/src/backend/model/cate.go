package model

import (
	"errors"
	"log"
)

type Category struct {
	//gorm.Model
	BaseModel
	Name   string `gorm:"not null;index" binding:"required,min=3,max=20"`
}

func (cate *Category) checkCate() error {
	cate.Name = PreventXSS(cate.Name)

	err := DB.Where("name = ?", cate.Name).Find(&cate).Error
	if err == nil {
		//说明该分类已经存在
		return errors.New("category has been existed")
	}
	return nil
}

func (cate *Category) Create() error {
	if err := cate.checkCate(); err != nil {
		return err
	}

	// create
	if err := DB.Create(&cate).Error; err != nil {
		log.Println(err)
		return errors.New("create category error")
	}

	return nil
}

func (cate *Category) Update(id int) error {
	if err := cate.checkCate(); err != nil {
		return err
	}

	upd := make(map[string]interface{})
	upd["name"] = cate.Name

	if err := DB.Where("id = ?", id).First(&cate).Error; err != nil {
		log.Println(err)
		return errors.New("category not existed")
	}

	if err := DB.Model(&cate).Updates(upd).Error; err != nil {
		log.Println(err)
		return errors.New("update category error")
	}

	return nil
}

// 分类是否存在，存在返回nil
func IsCateExisted(id uint) error {
	var cate Category
	err := DB.Select("id").Where("id = ?", id).Find(&cate).Error
	if err != nil {
		return errors.New("category not existed")
	}

	//说明该分类已经存在
	return nil
}
