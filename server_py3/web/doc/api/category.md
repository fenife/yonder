# category

## create
    ```
    POST    /api/category
    
    request headers:
        key: Cookie 
        val: token=fc3aeeebe31ba945cd1c076c6f2a9b2d
        
    request body:
    {
        "name": "aaa"
    }
    
    response:
    {
        "code": 0,
        "data": {
            "name": "aaa",
            "status": 1,
            "created_at": "2019-12-16 11:46:21",
            "updated_at": "2019-12-16 11:46:21",
            "id": 1
        },
        "msg": "OK"
    }
    ```

## update    
    ```
    PUT     /api/category/:cid
    
    request headers:
        key: Cookie 
        val: token=fc3aeeebe31ba945cd1c076c6f2a9b2d
        
    request body:
    {
        "name": "bbb"
    }
    
    response:
    {
        "code": 0,
        "data": {
            "name": "bbb",
            "status": 1,
            "created_at": "2019-12-16 11:46:21",
            "updated_at": "2019-12-16 11:46:21",
            "id": 1
        },
        "msg": "OK"
    }
    ```

## detail
    ```
    GET     /api/category/:cid
    
    response:
    {
        "code": 0,
        "data": {
            "name": "aaa",
            "status": 1,
            "created_at": "2019-12-16 11:46:21",
            "updated_at": "2019-12-16 11:46:21",
            "id": 1
        },
        "msg": "OK"
    }
    ```
    
## list
    ```
    GET     /api/category
    
    response:
    {
        "code": 0,
        "data": [
            {
                "id": 1,
                "created_at": "2019-12-16 11:46:21",
                "updated_at": "2019-12-16 11:46:21",
                "name": "aaa",
                "status": 1,
                "article_count": 5          # 该分类下可展示文章的数目
            }
        ],
        "msg": "OK"
    }
    ```