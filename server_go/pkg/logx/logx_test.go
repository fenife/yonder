package logx

import (
	"context"
	"fmt"
	"testing"
)

func TestLog(t *testing.T) {
	Debugf("debug msg")

	ctx := context.Background()
	Ctx(ctx).Infof("test ctx")

	Ctx(ctx).With("a", 1).With("b", 2).Warnf("warn msg")
	Ctx(ctx).With("a", 1, "b", 2).Warnf("warn msg2")

	ctx = context.WithValue(ctx, ctxKeyReqId, "reqId-123")
	Ctx(ctx).With("c", 3).Errorf("error msg")
	WithCtx(ctx).With("a", 1).Debugf("debug with ctx")

	With("a", 1).Infof("test with")
	WithError(fmt.Errorf("test err")).With("b", 2, "c", 3).Errorf("error msg")
}
