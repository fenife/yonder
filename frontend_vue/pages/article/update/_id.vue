<template>
  <div>
    <article-editor
      :user="user"
      :article="article"
      :cates="cates"
    >
    </article-editor>
  </div>
</template>

<script>
  import ArticleEditor from "~/components/article/Editor"
  import request from '~/api/request'

  export default {
    data () {
      return {
        user: this.$store.state.user,
        cates: this.$store.state.cates,
        // article: null,
      }
    },
    validate ({ params }) {
      // 必须是number类型
      return /^\d+$/.test(params.id)
    },
    asyncData (ctx) {
      // console.log("article asyncData")
      // console.log("params:", ctx.params)

      return Promise.all([
        request.getArticleDetail({
          client: ctx.req,
          params: {
            id: ctx.params.id
          }
        })
      ]).then(resp => {
        // console.log("get data:", resp)
        let article = resp[0].data.ad || null

        return {
          article: article
        }
      }).catch(err => {
        console.log("catch error:", err)
        ctx.error({ message: "not found", statusCode: 404 })
      })
    },
    components: {
      "article-editor": ArticleEditor,
    },
    layout: "nosidebar",
    middleware: "loginRequired"
  }
</script>
