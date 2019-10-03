<template>
  <div>
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
        pageSize: config.pageSize,
        articles: this.$store.state.articles,
        total: this.$store.state.total
      }
    },
    asyncData (ctx) {
      // console.log("index asyncData")
      return Promise.all([
        request.getCates({
          client: ctx.req
        }),
        request.getArticles({
          client: ctx.req,
        })
      ]).then(resp => {
        // console.log("get data:", resp)

        // categories
        let cates = resp[0].data.cateList || []
        // console.log("cates", cates)
        ctx.store.commit('setCates', cates)

        // articles
        let articles = resp[1].data.al || []
        // console.log("articles", articles)
        ctx.store.commit('setArticles', articles)

        let total = resp[1].data.total
        ctx.store.commit("setTotal", total)

        // return {
        //   articles: articles,
        //   total: total
        // }
      }).catch(err => {
        console.log("catch error:", err)
        ctx.error({ message: "not found", statusCode: 404 })
      })
    },
    methods: {
      onPageChange (page) {
        // console.log('get article list, page: ', page)
        request.getArticles({
          query: {
            page: page,
          }
        }).then(resp => {
          if (resp.code === 0) {
            // articles
            let articles = resp.data.al || []
            // console.log("articles", articles)
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
    layout: 'default',
    components: {
      'article-item': ArticleItem
    }
  }
</script>