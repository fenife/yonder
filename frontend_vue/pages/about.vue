<template>
  <div>
    <Card dis-hover>
      <div slot="title">
        <h1 class="article-title">{{article.title}}</h1>
        <div class="article-info">
          <span>{{article.user.name}}</span>
          <span>{{article.created_at}}</span>
        </div>
      </div>
      <ButtonGroup slot="extra" v-if="isAdmin">
        <article-tool :article="article"></article-tool>
      </ButtonGroup>

      <div class="article-content" >
        <div v-html="article.content"></div>
      </div>
    </Card>
    <!--todo: 添加文章目录 -->
  </div>
</template>

<script>
  import request from '~/api/request'
  import ArticleTool from '~/components/article/Tool'

  export default {
    data () {
      return {
        buttonSize: "small",
        isAdmin: this.$store.state.isAdmin,
      }
    },
    asyncData (ctx) {
      return Promise.all([
        request.getAbout({
          client: ctx.req,
          query: {
            ct: "html"
          }
        })
      ]).then(resp => {
        // console.log("get data:", resp)
        let result = resp[0]

        if (result.code !== 0) {
          ctx.error({ message: "not found", statusCode: 404 })
        }
        let article = result.data || {}
        return {
          article: article,
        }
      }).catch(err => {
        // console.log("catch error:", err)
        ctx.error({ message: "not found", statusCode: 404 })
      })
    },
    components: {
      "article-tool": ArticleTool,
    },
    layout: "nosidebar",
  }
</script>

<style lang="less" scoped>
  .article-title {
    margin-bottom: 10px;
  }
  .article-info {
    /*margin: 5px 8px;*/
  }
  .article-content {
    padding: 0 12px;
    font-size: 16px;

    p {
      padding: 8px;
    }
  }
</style>