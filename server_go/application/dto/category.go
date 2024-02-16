/*
Data Transfer Object (dto)
一个领域(domain)里的对象可以用 entity 或者 do 里的对象表示；
当涉及多个领域的数据，需要进行聚合时，可以在 dto 里定义
*/

package dto

type CategoryList struct {
	CateId    uint64 `json:"cate_id"`    // 分类id
	CateName  string `json:"cate_name"`  // 分类名称
	PostCount int    `json:"post_count"` // 该分类下的文章数
}

type CategoryBrief struct {
	ID        uint64 `json:"id"`
	CreatedAt string `json:"created_at"` // "2006-01-02 15:05:05"
	UpdatedAt string `json:"updated_at"` // 同上
	Name      string `json:"name"`
}
