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
    state.isAdmin = (user && (user.Role === UserRoleAdmin))
  },
  setSearch (state, q) {
    state.q = q
  }
}

export const actions = {
  nuxtServerInit( { commit }, { req } ) {
    // console.log(commit)
    // console.log('nuxtServerInit', req.headers)
    Promise.all([
      request.getUserInfo({ client: req }),
    ]).then( (resp) => {
      let user = resp[0].data.user
      // console.log('nuxtServerInit', user)
      commit("setUser", user)
      // next()
    }).catch( (err) => {
      console.log(err)
    })
  }
}

// export default store
