package logx

import "context"

type Loggerx interface {
	Ctx(ctx context.Context) Loggerx
	With(keyAndValues ...interface{}) Loggerx
	Debugf(msg string, args ...interface{})
	Infof(msg string, args ...interface{})
	Warnf(msg string, args ...interface{})
	Errorf(msg string, args ...interface{})
	Panicf(msg string, args ...interface{})
}

var innerLogger *InnerLogger

func InitLogger() {
	innerLogger = NewInnerLogger()
}

func Ctx(ctx context.Context) Loggerx {
	l := NewInnerLogger()
	l.ctx = ctx
	return l
}

func Debugf(msg string, args ...interface{}) {
	innerLogger.Debugf(msg, args...)
}

func Infof(msg string, args ...interface{}) {
	innerLogger.Infof(msg, args...)
}

func Warnf(msg string, args ...interface{}) {
	innerLogger.Warnf(msg, args...)
}

func Errorf(msg string, args ...interface{}) {
	innerLogger.Errorf(msg, args...)
}

func Panicf(msg string, args ...interface{}) {
	innerLogger.Panicf(msg, args...)
}

func init() {
	InitLogger()
}
