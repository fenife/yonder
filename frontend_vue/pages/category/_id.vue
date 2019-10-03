<template>
  <div>
    <Card :bordered="false" class="category-info">
      <p slot="title" class="title">category</p>
      <p class="content">{{cate.Name}}</p>
    </Card>

    <article-item
      v-for="ar in articles"
      :article="ar"
      :key="ar.ID"
    >
    </article-item>

    <Page
      v-if="total > pageSize"
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
    validate ({ params }) {
      // 必须是number类型
      return /^\d+$/.test(params.id)
    },
    data () {
      return {
        pageSize: config.pageSize,
        cate: this.$store.state.cate,
        articles: this.$store.state.articles,
        total: this.$store.state.total,
      }
    },
    asyncData (ctx) {
      // console.log("article asyncData")
      // console.log("params:", ctx.params)
      // console.log("query:", ctx.query)
      let cateId = ctx.params.id
      // 优化：分类列表可以不用每次都获取

      return Promise.all([
        request.getCates({
          client: ctx.req
        }),
        request.getArticles({
          client: ctx.req,
          query: {
            cateId: cateId
          }
        })
      ]).then(resp => {
        // console.log("get data:", resp)
        // categories
        let cates = resp[0].data.cateList || []
        ctx.store.commit('setCates', cates)

        // 取出当前所属分类的详细信息
        let cate = {}
        for (let c of cates) {
          if (c.ID.toString() === cateId) {
            cate = c
            break
          }
        }
        ctx.store.commit('setCate', cate)

        // articles
        let articles = resp[1].data.al || []
        ctx.store.commit('setArticles', articles)

        let total = resp[1].data.total || 0
        ctx.store.commit('setTotal', total)
      }).catch(err => {
        console.log("catch error:", err)
        ctx.error({ message: "not found", statusCode: 404 })
      })
    },
    methods: {
      onPageChange (page) {
        console.log('get article list, page: ', page)
        request.getArticles({
          query: {
            cateId: this.cate.ID,
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
      },
    },
    layout: "default",
    components: {
      'article-item': ArticleItem
    }
  }
</script>

<style scoped>
  .category-info {
    margin-bottom: 8px;
  }
  .category-info .title, .category-info .content {
    font-size: 16px;
  }
</style>
