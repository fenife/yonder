const axios = require('axios')
const apiList = require('~/api/api')

function send(key, options) {
  return new Promise( (resolve, reject) => {
    let apiConf = apiList[key]
    options = options || {}
    apiConf.method = apiConf.method.toLocaleLowerCase()
    let url = apiConf.url

    // url: /articles/:id
    // params: { id: 1 }
    if (options.params) {
      let params = options.params
      // console.log("params:", params)
      for (let key in params) {
        if (params.hasOwnProperty(key)) {
          url = url.replace(":" + key, params[key])
        }
      }
    }

    // url: /articles
    // query: { page: 1, rows: 10 }
    if (options.query) {
      let query = options.query
      let queryArr = []
      for (let key in query) {
        if (query.hasOwnProperty(key)) {
          queryArr.push(key + '=' + query[key])
        }
      }
      if (queryArr.length > 0) {
        url += '?' + queryArr.join('&')
      }
    }

    // console.log("url:", url)

    let axiosConf = {
      method: apiConf.method,
      url: url,
      headers: {}
    }

    // headers
    let client = options.client
    if (typeof window === 'undefined' && !client) {
      throw new Error(key + ":client can not be null")
    }
    if (client && client.headers) {
      if (client.headers['user-agent']) {
        axiosConf.headers['User-Agent'] = client.headers['user-agent']
      }
      if (client.headers['cookie']) {
        axiosConf.headers['Cookie'] = client.headers['cookie']
      }
    }

    // body
    if (apiConf.method === 'post' || apiConf.method === 'put') {
      axiosConf.data = options.body || {}
    }

    // console.log("axios config:", axiosConf)

    // request
    axios(axiosConf)
      .then( function (response) {
        return resolve(response.data)
      })
      .catch( function (error) {
        return reject(error)
      })
  })
}

const req = {}

for (let key in apiList) {
  if (apiList.hasOwnProperty(key)) {
    req[key] = (options) => {
      return send(key, options)
    }
  }
}

export default req
