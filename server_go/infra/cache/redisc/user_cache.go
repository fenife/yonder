package redisc

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/redis/go-redis/v9"
	"server-go/domain/cache"
	"server-go/domain/entity"
	"strconv"
	"time"
)

const (
	userCacheExpired = 60 * time.Second

	prefixIdToUser  = "id2user:"
	prefixTokenToId = "token2id:"
)

type UserCache struct {
	rds *redis.Client
}

func NewUserCache(rds *redis.Client) *UserCache {
	return &UserCache{
		rds: rds,
	}
}

// UserRepo implements the repo.UserRepo interface
var _ cache.IUserCache = &UserCache{}

func (u *UserCache) CacheUserByToken(ctx context.Context, token string, user *entity.User) error {
	userData, err := json.Marshal(user)
	if err != nil {
		return err
	}

	pipe := u.rds.TxPipeline()
	// 保存用户token到id的映射关系, token2id:<token> -> uid
	pipe.Set(ctx, getKeyToken2Id(token), user.ID, userCacheExpired)
	// 根据用户id缓存用户信息, id2user:<uid> -> user
	pipe.Set(ctx, getKeyId2User(user.ID), userData, userCacheExpired)
	_, err = pipe.Exec(ctx)
	return err
}

func (u *UserCache) GetUserByToken(ctx context.Context, token string) (*entity.User, error) {
	// 先获取token对应的用户id
	uidStr, err := u.rds.Get(ctx, getKeyToken2Id(token)).Result()
	if err != nil {
		return nil, err
	}
	uid, err := strconv.ParseUint(uidStr, 10, 64)
	if err != nil {
		return nil, err
	}
	// 根据用户id获取用户信息
	return u.GetUserById(ctx, uid)
}

func (u *UserCache) GetUserById(ctx context.Context, userId uint64) (*entity.User, error) {
	userData, err := u.rds.Get(ctx, getKeyId2User(userId)).Result()
	if err == redis.Nil || userData == "" {
		return &entity.User{}, nil
	}
	if err != nil {
		return nil, err
	}
	var user entity.User
	err = json.Unmarshal([]byte(userData), &user)
	return &user, err
}

func getKeyId2User(uid uint64) string {
	return fmt.Sprintf("%s:%d", prefixIdToUser, uid)
}

func getKeyToken2Id(token string) string {
	return fmt.Sprintf("%s:%s", prefixTokenToId, token)
}
