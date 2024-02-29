// let config = require('~/config')
import config from '~/config'

// let baseUrl = config.baseUrl
let apiV1 = config.goServer + "/api/v1"
let baseUrl = apiV1

if (typeof window === 'undefined') {
  // baseUrl = config.pyurl
  // gourl = config.gourl
  apiV1 = config.goServer + "/api/v1"
  baseUrl = apiV1
}

const apiList = {
  // 获取文章列表
  getArticles: {
    url: apiV1 + "/post/list",
    method: "GET"
  },
  // 获取文章详情
  getArticleDetail: {
    url: baseUrl + "/post/detail",
    method: "GET"
  },

  // 新建文章
  createArticle: {
    url: baseUrl + "/article/create",
    method: "POST"
  },

  // 更新文章
  updateArticle: {
    // url: baseUrl + "/article/:id",
    url: baseUrl + "/article/update",
    method: "PUT"
  },

  // 删除文章
  deleteArticle: {
    url: baseUrl + "/article/:id",
    method: "DELETE"
  },

  // 分类列表
  getCates: {
    url: apiV1 + "/category/list",
    method: "GET"
  },
  // 分类详情
  getCateDetail: {
    // url: baseUrl + "/category/:id",
    url: baseUrl + "/category/detail",
    method: "GET"
  },
  // 新建分类
  createCate: {
    url: baseUrl + "/category/create",
    method: "POST"
  },
  // 更新分类
  updateCate: {
    // url: baseUrl + "/category/:id",
    url: baseUrl + "/category/update",
    method: "PUT"
  },
  // 删除分类
  deleteCate: {
    url: baseUrl + "/category/:id",
    method: "DELETE"
  },

  // 登陆
  signin: {
    url: baseUrl + "/user/signin",
    method: "POST"
  },
  signout: {
    url: baseUrl + "/user/signout",
    method: "GET"
  },
  getUserInfo: {
    url: baseUrl + "/user/info",
    method: "GET"
  },

  // todo: 注册

  // 搜索
  searchArticle: {
    url: baseUrl + "/post/search",
    // url: baseUrl + "/v2/search",
    // url: baseUrl + "/v3/search",
    method: "GET"
  },

  // 归档页面
  getArchive: {
    url: apiV1 + "/post/archive",
    method: "GET"
  },

  // 关于页面
  getAbout: {
    url: apiV1 + '/post/about',
    method: "GET"
  },
}

// module.exports = apiList
// module.exports = {
//   apiList
// };
export default apiList
