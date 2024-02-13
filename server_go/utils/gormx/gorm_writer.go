package gormx

import (
	"gorm.io/gorm/logger"
	"server-go/utils/logx"
)

type gormWriter struct{}

func NewGormWriter() logger.Writer {
	return &gormWriter{}
}

func (w *gormWriter) Printf(msg string, data ...interface{}) {
	logx.Infof(msg, data...)
}
