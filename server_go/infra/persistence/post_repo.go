package persistence

import (
	"context"
	"errors"
	"gorm.io/gorm"
	"server-go/domain/do"
	"server-go/domain/entity"
	"server-go/domain/repo"
)

type PostRepo struct {
	db *gorm.DB
}

func NewPostRepo(db *gorm.DB) *PostRepo {
	return &PostRepo{db}
}

// UserRepo implements the repo.UserRepo interface
var _ repo.IPostRepo = &PostRepo{}

func (r *PostRepo) GetPostStat(ctx context.Context) ([]do.PostStat, error) {
	var postStats []do.PostStat
	err := r.db.WithContext(ctx).Model(&entity.Post{}).
		Select("cate_id", "count(1) as post_count").Group("cate_id").
		Find(&postStats).Error
	return postStats, err
}

func (r *PostRepo) GetPostList(ctx context.Context, cateId uint64, page, limit int) ([]*entity.Post, error) {
	var posts []*entity.Post
	tx := r.db.WithContext(ctx)
	if cateId > 0 {
		tx = tx.Where("cate_id = ?", cateId)
	}
	offset := (page - 1) * limit
	err := tx.Omit("content").Preload("User").Preload("Category").Offset(offset).Limit(limit).Find(&posts).Error
	return posts, err
}

func (r *PostRepo) GetPostArchiveList(ctx context.Context) ([]*entity.Post, error) {
	// 默认按id倒序排序，亦即创建时间(create_at)
	var posts []*entity.Post
	err := r.db.WithContext(ctx).Preload("User").Preload("Category").
		Omit("content").Order("id desc").Find(&posts).Error
	return posts, err
}

func (r *PostRepo) FindById(ctx context.Context, postId uint64) (*entity.Post, error) {
	var post entity.Post
	err := r.db.WithContext(ctx).Where("id = ?", postId).Preload("User").Preload("Category").First(&post).Error
	if errors.Is(err, gorm.ErrRecordNotFound) {
		// 可通过ID判断是否存在
		return &post, nil
	}
	return &post, err
}

func (r *PostRepo) FindByTitle(ctx context.Context, name string) (*entity.Post, error) {
	var post entity.Post
	err := r.db.WithContext(ctx).Where("title = ?", name).Preload("User").Preload("Category").First(&post).Error
	if errors.Is(err, gorm.ErrRecordNotFound) {
		// 通过ID判断是否存在
		return &post, nil
	}
	return &post, err
}

func (r *PostRepo) SearchByTitle(ctx context.Context, kw string, page, limit int) ([]*entity.Post, error) {
	var posts []*entity.Post
	offset := (page - 1) * limit
	err := r.db.WithContext(ctx).Preload("User").Preload("Category").
		Omit("content").Where("title like ?", "%"+kw+"%").Order("id desc").
		Offset(offset).Limit(limit).Find(&posts).Error
	return posts, err
}

func (r *PostRepo) GetPrePost(ctx context.Context, postId uint64) (*entity.Post, error) {
	var post entity.Post
	err := r.db.WithContext(ctx).Preload("User").Preload("Category").
		Where("id < ?", postId).Order("id desc").First(&post).Error
	if errors.Is(err, gorm.ErrRecordNotFound) {
		// 可通过ID判断是否存在
		return &post, nil
	}
	return &post, err
}

func (r *PostRepo) GetNextPost(ctx context.Context, postId uint64) (*entity.Post, error) {
	var post entity.Post
	err := r.db.WithContext(ctx).Preload("User").Preload("Category").
		Where("id > ?", postId).Order("id asc").First(&post).Error
	if errors.Is(err, gorm.ErrRecordNotFound) {
		// 可通过ID判断是否存在
		return &post, nil
	}
	return &post, err
}
