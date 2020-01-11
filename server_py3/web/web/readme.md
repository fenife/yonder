# api & desc
    1. 一个api对应一个文件，且该文件中包含该api的描述文档

    2. 描述文档可通过http请求查看
    2.1) 该文档的url = api url + '/desc'
    2.2) 该文档的url method最好跟api的保持一致
       
    2.3) 比如：
        api 为 'POST /api/article/create'
        则其描述文档的url为：
        'POST /api/article/create/desc'
    
    3. 以desc结尾的api url归为描述文档一类，需要权限才能查看
       在middleware中进行权限检查及拦截
