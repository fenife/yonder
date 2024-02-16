package dto

type UserBrief struct {
	ID        uint64 `json:"id"`
	CreatedAt string `json:"created_at"` // "2006-01-02 15:05:05"
	UpdatedAt string `json:"updated_at"` // 同上
	Name      string `json:"name"`
}
