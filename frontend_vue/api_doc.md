# api doc
    method: GET

## article list
    target: 
        pages/index.vue
        components/article/Item.vue
        
    url: api/articles
    
    ```json
    {
        "code": 0,
        "msg": "success",
        "data": {
            "al": [
                {
                    "ID": 1,
                    "CreatedAt": "2019-05-03T18:46:48+08:00",
                    "UpdatedAt": "2019-05-26T12:24:05+08:00",
                    "Title": "python",
                    "UserId": 1,
                    "Username": "admin",
                    "CateId": 2,
                    "CateName": "java"
                },
                {
                    "ID": 2,
                    "CreatedAt": "2019-05-03T18:47:58+08:00",
                    "UpdatedAt": "2019-05-03T18:47:58+08:00",
                    "Title": "java",
                    "UserId": 1,
                    "Username": "admin",
                    "CateId": 1,
                    "CateName": "lua"
                }
            ]
        }
    }
    ```
    
## category list
    target: 
        pages/index.vue
        components/CateItem.vue
        
    url: api/categories
    
    ```json
    {
        "code": 0,
        "msg": "success",
        "data": {
            "cateList": [
                {
                    "ID": 1,
                    "CreatedAt": "2019-05-03T18:46:33+08:00",
                    "UpdatedAt": "2019-05-03T18:46:33+08:00",
                    "DeletedAt": null,
                    "Name": "lua"
                },
                {
                    "ID": 2,
                    "CreatedAt": "2019-05-25T18:25:20+08:00",
                    "UpdatedAt": "2019-05-25T18:25:20+08:00",
                    "DeletedAt": null,
                    "Name": "java"
                }
            ]
        }
    }
    ```

## article detail
    target:
        pages/articles/_id.vue
      
    url: api/article/:id

    ```json
    {
        "code": 0,
        "msg": "success",
        "data": {
            "ad": {
                "ID": 2,
                "CreatedAt": "2019-05-03T18:47:58+08:00",
                "UpdatedAt": "2019-05-03T18:47:58+08:00",
                "DeletedAt": null,
                "UserId": 1,
                "CateId": 1,
                "Title": "java",
                "Content": "java",
                "User": {
                    "ID": 1,
                    "CreatedAt": "2019-05-03T18:46:04+08:00",
                    "UpdatedAt": "2019-05-03T18:46:04+08:00",
                    "DeletedAt": null,
                    "Name": "admin",
                    "Role": 1,
                    "Status": 1
                },
                "Category": {
                    "ID": 1,
                    "CreatedAt": "2019-05-03T18:46:33+08:00",
                    "UpdatedAt": "2019-05-03T18:46:33+08:00",
                    "DeletedAt": null,
                    "Name": "lua"
                }
            }
        }
    }
    ```
    
## signin
    target: pages/signin.vue
    
    url: /api/user/login
    method: POST
    body: 
    ```json
    {
    	"name": "username",
    	"password": "xxx"
    } 
    ```
    
    result:
    ```json
    {
        "code": 0,
        "data": {
            "token": "64b85f6b6bf2bb39eaffc25deecaefc2",
            "user": {
                "ID": 1,
                "CreatedAt": "2019-05-03T18:46:04+08:00",
                "UpdatedAt": "2019-05-03T18:46:04+08:00",
                "DeletedAt": null,
                "Name": "admin",
                "Role": 1,
                "Status": 1
            }
        },
        "msg": "success"
    }
    ```