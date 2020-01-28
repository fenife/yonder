# 搜索
    ses: search service
    
## stopwords
    see: https://github.com/goto456/stopwords.git
    
## api service 
    搜索api服务，会调用engine中的函数，
    通过api提交文档建立索引，
    通过api获取搜索结果，
    
    不做权限验证，由其他服务保证，
    所以只限本地服务调用，不开放公网访问

## engine
    搜索引擎，
    建立索引，
    根据关键字查询索引获取结果，
    保存索引和源数据
