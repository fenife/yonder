<template>
  <div>
    <Card :bordered="false" class="search-info">
      <p slot="title" class="title">search:</p>
      <p class="content">{{q}}</p>
    </Card>
    <article-item
      v-for="ar in articles"
      :article="ar"
      :key="ar.ID"
    >
    </article-item>
    <Page
      v-if="total > pageSize "
      :total="total"
      :page-size="pageSize"
      @on-change="onPageChange"
    ></Page>
    <!--<div v-for="ar in articles">{{ar}}</div>-->
  </div>
</template>

<script>
  import request from '~/api/request'
  import ArticleItem from '~/components/article/Item'
  import config from '~/config'

  export default {
    data () {
      return {
        q: this.$store.state.q,
        pageSize: config.pageSize,
        articles: this.$store.state.articles,
        total: this.$store.state.total,
      }
    },
    asyncData (ctx) {
      // console.log("article asyncData")
      // console.log("params:", ctx.params)
      // console.log("query:", ctx.query)
      let searchValue = ctx.params.q
      // 优化：分类列表可以不用每次都获取
      return Promise.all([
        request.getCates({
          client: ctx.req
        }),
        request.searchArticle({
          client: ctx.req,
          query: {
            q: searchValue
          }
        })
      ]).then(resp => {
        ctx.store.commit('setSearch', searchValue)
        // console.log("get data:", resp)
        // categories
        let cates = resp[0].data.cateList || []
        ctx.store.commit('setCates', cates)

        // articles
        let articles = resp[1].data.al || []
        ctx.store.commit('setArticles', articles)

        let total = resp[1].data.total || 0
        ctx.store.commit('setTotal', total)

        // return {
        //   q: searchValue,
        //   articles: articles
        // }
      }).catch(err => {
        console.log("catch error:", err)
        ctx.error({ message: "not found", statusCode: 404 })
      })
    },
    methods: {
      onPageChange (page) {
        // console.log('get article list, page: ', page)
        request.searchArticle({
          query: {
            q: this.q,
            page: page,
          }
        }).then(resp => {
          if (resp.code === 0) {
            // articles
            let articles = resp.data.al || []
            this.$store.commit('setArticles', articles)
            this.articles = articles

            let total = resp.data.total
            this.$store.commit("setTotal", total)
            this.total = total
          } else {
            this.$Message.error({
              duration: 3,
              closable: true,
              content: resp.message || resp.msg,
            })
          }
        }).catch(err => {
          this.$Message.error({
            duration: 3,
            closable: true,
            content: err.message || err.msg,
          })
        })
      }
    },
    layout: "default",
    components: {
      'article-item': ArticleItem
    }
  }
</script>

<style scoped>
  .search-info {
    margin-bottom: 8px;
  }
  .search-info .title, .search-info .content {
    font-size: 16px;
  }
</style>
