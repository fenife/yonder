package logx

import (
	"context"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

const ctxKeyReqId = "request_id"

type InnerLogger struct {
	zapLogger *zap.Logger
	ctx       context.Context
	fields    []interface{}
}

func NewInnerLogger() *InnerLogger {
	//encoderCfg := zapcore.EncoderConfig{
	//	TimeKey:       "ts",
	//	LevelKey:      "level",
	//	NameKey:       "logger",
	//	CallerKey:     "caller",
	//	FunctionKey:   "func",
	//	MessageKey:    "msg",
	//	StacktraceKey: "stacktrace",
	//	LineEnding:    zapcore.DefaultLineEnding,
	//	EncodeLevel:   zapcore.LowercaseLevelEncoder,
	//	//EncodeTime:     zapcore.RFC3339TimeEncoder,
	//	EncodeTime: zapcore.TimeEncoderOfLayout("2006-01-02 15:05:05.000"),
	//
	//	EncodeDuration: zapcore.SecondsDurationEncoder,
	//	EncodeCaller:   zapcore.ShortCallerEncoder,
	//}
	//core := zapcore.NewCore(
	//	zapcore.NewJSONEncoder(encoderCfg),
	//	os.Stdout,
	//	zap.DebugLevel,
	//)
	//zapLogger := zap.New(core)
	config := zap.NewProductionConfig()
	config.EncoderConfig.EncodeTime = zapcore.TimeEncoderOfLayout("2006-01-02 15:05:05.000")
	config.Level = zap.NewAtomicLevelAt(zap.DebugLevel)
	//config.EncoderConfig.FunctionKey = "func"
	zapLogger, err := config.Build()
	if err != nil {
		panic(err)
	}

	return &InnerLogger{
		zapLogger: zapLogger,
		fields:    make([]interface{}, 0),
	}
}

func (l *InnerLogger) Ctx(ctx context.Context) Loggerx {
	l.ctx = ctx
	return l
}

func (l *InnerLogger) With(keyAndValues ...interface{}) Loggerx {
	if l.ctx != nil {
		if val, ok := l.ctx.Value(ctxKeyReqId).(string); ok {
			l.fields = append(l.fields, ctxKeyReqId, val)
		}
	}
	l.fields = append(l.fields, keyAndValues...)
	return l
}

func (l *InnerLogger) buildFields() []interface{} {
	return l.fields
}

func (l *InnerLogger) Debugf(msg string, args ...interface{}) {
	fields := l.buildFields()
	if len(fields) > 0 {
		l.zapLogger.Sugar().With(fields...).Debugf(msg, args...)
	} else {
		l.zapLogger.Sugar().Debugf(msg, args...)
	}
}

func (l *InnerLogger) Infof(msg string, args ...interface{}) {
	fields := l.buildFields()
	if len(fields) > 0 {
		l.zapLogger.Sugar().With(fields...).Infof(msg, args...)
	} else {
		l.zapLogger.Sugar().Infof(msg, args...)
	}
}

func (l *InnerLogger) Warnf(msg string, args ...interface{}) {
	fields := l.buildFields()
	if len(fields) > 0 {
		l.zapLogger.Sugar().With(fields...).Warnf(msg, args...)
	} else {
		l.zapLogger.Sugar().Warnf(msg, args...)
	}
}

func (l *InnerLogger) Errorf(msg string, args ...interface{}) {
	//l.zapLogger.Sugar().With(l.buildFields()).Errorf(msg, args...)
	fields := l.buildFields()
	if len(fields) > 0 {
		l.zapLogger.Sugar().With(fields...).Errorf(msg, args...)
	} else {
		l.zapLogger.Sugar().Errorf(msg, args...)
	}
}

func (l *InnerLogger) Panicf(msg string, args ...interface{}) {
	//l.zapLogger.Sugar().With(l.buildFields()).Panicf(msg, args...)
	fields := l.buildFields()
	if len(fields) > 0 {
		l.zapLogger.Sugar().With(fields...).Panicf(msg, args...)
	} else {
		l.zapLogger.Sugar().Panicf(msg, args...)
	}
}
