// domain object

package do

import "time"

const signinInternalLimit = 30 // 登陆限制，多少秒内只能登陆一次，一般小于 userCacheExpired

type UserSignInInfo struct {
	Token  string `json:"token"`
	UserId uint64 `json:"user_id"`
	SignTs int64  `json:"sign_ts"`
}

func (s *UserSignInInfo) IsSignInLimit() bool {
	return time.Now().Unix()-s.SignTs < signinInternalLimit
}
