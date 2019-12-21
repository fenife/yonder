# archive
    ```
    GET     /api/archive
    
    response:
    {
        "code": 0,
        "data": {
            "2018": {
                "year": 2018,
                "art_list": [
                    {
                        "id": 1,
                        "title": "aaaaa",
                        "created_at": "2018-12-15 17:43:19",
                        "updated_at": "2019-12-16 22:54:19"
                    }
                ],
                "count": 1
            },
            "2019": {
                "year": 2019,
                "art_list": [
                    {
                        "id": 4,
                        "title": "fdsafdds",
                        "created_at": "2019-12-15 17:51:55",
                        "updated_at": "2019-12-15 17:51:55"
                    },
                    {
                        "id": 5,
                        "title": "fdsafdads",
                        "created_at": "2019-12-15 17:52:40",
                        "updated_at": "2019-12-15 17:52:40"
                    }
                ],
                "count": 2
            }
        },
        "msg": "OK"
    } 
    ```
