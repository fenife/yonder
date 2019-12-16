# user

## signup
    ```
    POST    /api/user/signin
    
    body:
    {
        "username": "abc",
        "password": "abc"
    }
    
    response:
    {
        "code": 0,
        "data": {
            "name": "abc",
            "status": 1,
            "role_id": 2,
            "created_at": "2019-12-16 11:51:15",
            "updated_at": "2019-12-16 11:51:15",
            "id": 3
        },
        "msg": "OK"
    }
    ```
    
## signin
    ```
    POST    /api/user/signin
    
    body:
    {
        "username": "abc",
        "password": "abc"
    }
    
    response header:
        key: Set-Cookie  
        val: token=3cf239884c6acda909735d7bc0cb8259; Max-Age=600; Path=/
    
    response body:
    {
        "code": 0,
        "data": {
            "name": "abc",
            "status": 1,
            "role_id": 2,
            "created_at": "2019-12-16 11:51:15",
            "updated_at": "2019-12-16 11:51:15",
            "id": 3
        },
        "msg": "OK"
    }
    ```    
    
## login user info
    ```
    GET     /api/user/info
    
    request headers:
        key: Cookie 
        val: token=fc3aeeebe31ba945cd1c076c6f2a9b2d
        
    response:
    {
        "code": 0,
        "data": {
            "id": 3,
            "created_at": "2019-12-16 11:51:15",
            "updated_at": "2019-12-16 11:51:15",
            "name": "abc",
            "role_id": 2,
            "status": 1
        },
        "msg": "OK"
    }
    ```
    
## user detail
    ```
    GET     /api/user/:uid
    
    # todo:
    # permission require: admin 
    # only admin can get user detail, avoid user info leakage
    
    response:
    {
        "code": 0,
        "data": {
            "id": 3,
            "created_at": "2019-12-16 11:51:15",
            "updated_at": "2019-12-16 11:51:15",
            "name": "abc",
            "role_id": 2,
            "status": 1
        },
        "msg": "OK"
    }
    ```

## user update
    ```
    PUT     /api/user/:uid
    
    request headers:
        key: Cookie 
        val: token=fc3aeeebe31ba945cd1c076c6f2a9b2d
        
    request body:
    {
        "username": "abc",
        "password": "abc"
    }
    
    response:
    {
        "code": 0,
        "data": {
            "name": "abc",
            "status": 1,
            "created_at": "2019-12-16 11:46:21",
            "updated_at": "2019-12-16 11:46:21",
            "id": 1
        },
        "msg": "OK"
    }
    ```