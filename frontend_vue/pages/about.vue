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
    <!-- 添加文章目录 -->
    <div v-if="toc" class="catalogue">
      <Card dis-hover>
        <div class="article-toc">
          <div v-html="toc"></div>
        </div>
      </Card>
    </div>

    <Back-top></Back-top>

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
        if (resp[0].code !== 0) {
          ctx.error({ message: "not found", statusCode: 404 })
        }

        let result = resp[0].data
        let article = result.article || {}
        let toc = result.toc
        return {
          article: article,
          toc: toc,
        }
      }).catch(err => {
        // console.log("catch error:", err)
        ctx.error({ message: "not found", statusCode: 404 })
      })
    },
    components: {
      "article-tool": ArticleTool,
    },
    layout: "detail",
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

  .catalogue {
    position: fixed;
    top: 70px;
    right: 0.5rem;
    cursor: pointer;
    display: flex;
  }
</style>