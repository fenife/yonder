package model

import (
	"backend/utils"
	"github.com/microcosm-cc/bluemonday"
)

type BaseModel struct {
	ID        uint            `gorm:"primary_key"`
	CreatedAt utils.JSONTime
	UpdatedAt utils.JSONTime
	DeletedAt *utils.JSONTime `sql:"index"`
}

// It protects sites from XSS attacks
func PreventXSS(input string) string {
	return bluemonday.UGCPolicy().Sanitize(input)
}