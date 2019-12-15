# article api

## create
    ```
    POST  /api/article
    
    {
        "title": "aaa",
        "content": "abc",
        "cate_id": 1
    }
    
    response:
    {
        "code": 0,
        "data": {
            "user_id": 1,
            "cate_id": 1,
            "title": "aaa",
            "content": "abc",
            "status": 1,
            "created_at": "2019-12-15 17:57:46",
            "updated_at": "2019-12-15 17:57:46",
            "id": 1
        },
        "msg": "OK"
    }
    ```
    
## update  
