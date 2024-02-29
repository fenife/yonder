import Vue from 'vue'
import Vuex from 'vuex'
import request from '~/api/request'

Vue.use(Vuex)

// const store = () => new Vuex.Store({
//   state: {
//     cates: [],
//     articles: []
//   },
//   mutations: {
//     setCates (state, cates) {
//       state.cates = cates
//     },
//     setArticles (state, articles) {
//       state.articles = articles
//     }
//   }
// })

const UserRoleAdmin = 1

import { setTokenCookie } from "../libs/util";

export const state = () => ({
  // todo: isAdmin set to false
  isAdmin: false,
  cates: [],
  articles: [],
  total: 0,
  cate: null,
  token: null,
  user: null,
  q: '',
})

export const mutations = {
  setCates (state, cates) {
    state.cates = cates
  },
  setCate (state, cate) {
    state.cate = cate
  },
  setArticles (state, articles) {
    state.articles = articles
  },
  setTotal (state, total) {
    state.total = total
  },
  setToken (state, token) {
    state.token = token
    setTokenCookie(token)
  },
  setUser (state, user) {
    state.user = user
    state.isAdmin = (user && (user.role_id === UserRoleAdmin))
  },
  setSearch (state, q) {
    state.q = q
  }
}

export const actions = {
  nuxtServerInit( { commit }, { req } ) {
    let user = {}
    commit("setUser", user)
    // console.log(commit)
    // console.log('nuxtServerInit', req.headers)
    // Promise.all([
    //   request.getUserInfo({ client: req }),
    // ]).then( (resp) => {
    //   // console.log('nuxtServerInit, resp', resp)
    //   let user = resp[0].data
    //
    //   // 如果是空对象{}，要转化为null，否则后面vue判断user是否存在时会出错，eg:
    //   // Header.vue, v-if="user"
    //   // 判断user是否为空对象{}；如果是{}，则肯定不存在属性id
    //   // 也有其他的判断方法，具体可google
    //   // if (!user.id) {
    //   //   user = null
    //   // }
    //   // console.log('nuxtServerInit, user:', user)
    //   commit("setUser", user)
    //   // next()
    // }).catch( (err) => {
    //   console.log(err)
    // })
  }
}

// export default store
