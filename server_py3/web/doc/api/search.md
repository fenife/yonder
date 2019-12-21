# search
    ```
    GET     /api/search
    
    required params:
        kw: 搜索关键字
         
    optional params:
        page   : 第几页，要大于0
        limit  : 一页显示的文章数目
        
        eg:
        /api/search?kw='aaa'&page=1&limit=2
    
    response:
    {
        "code": 0,
        "data": {
            "articles": [
                {
                    "id": 1,
                    "title": "aaaaa",
                    "created_at": "2018-12-15 17:43:19",
                    "updated_at": "2019-12-16 22:54:19",
                    "user_id": 1,
                    "user_name": "admin",
                    "cate_id": 1,
                    "cate_name": "cccc"
                },
                {
                    "id": 8,
                    "title": "aaaaaa",
                    "created_at": "2019-12-16 22:54:59",
                    "updated_at": "2019-12-16 22:54:59",
                    "user_id": 1,
                    "user_name": "admin",
                    "cate_id": 1,
                    "cate_name": "cccc"
                }
            ]
        },
        "msg": "OK"
    }
    ```