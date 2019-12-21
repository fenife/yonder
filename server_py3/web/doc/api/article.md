# article api

## create
    ```
    POST  /api/article
    
    request headers:
        key: Cookie 
        val: token=fc3aeeebe31ba945cd1c076c6f2a9b2d
       
    request body:   
    {
        "title": "aaa",
        "content": "abc",
        "cate_id": 1
    }
    
    response body:
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
    同 create

## article list
    ```
    GET     /api/article
    
    optional params:
        cate_id: 1
        page   : 1
        limit  : 2
        
        eg:
        /api/article?cate_id=1&page=1&limit=2
    
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
                    "id": 2,
                    "title": "hello worlda",
                    "created_at": "2018-12-15 17:44:31",
                    "updated_at": "2019-12-15 17:44:31",
                    "user_id": 1,
                    "user_name": "admin",
                    "cate_id": 1,
                    "cate_name": "cccc"
                }
            ],
            "total": 10
        },
        "msg": "OK"
    }
    ```

## detail
    ```
    GET     /api/article/:aid
    
    response:
    {
        "code": 0,
        "data": {
            "id": 1,
            "created_at": "2019-12-15 17:43:19",
            "updated_at": "2019-12-15 17:43:19",
            "user_id": 1,
            "cate_id": 1,
            "title": "aaa",
            "content": "abc",
            "status": 1
        },
        "msg": "OK"
    }
    ```
