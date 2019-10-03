<template>
  <div>
    <div>
      <Card dis-hover>
        <Breadcrumb>
          <BreadcrumbItem to="/">Home</BreadcrumbItem>
          <BreadcrumbItem :to="`/category/${article.Category.ID}`">{{article.Category.Name}}</BreadcrumbItem>
          <BreadcrumbItem>{{article.Title}}</BreadcrumbItem>
        </Breadcrumb>
      </Card>
    </div>
    <Card dis-hover>
      <div slot="title">
        <h1 class="article-title">{{article.Title}}</h1>
        <div class="article-info">
          <span>{{article.User.Name}}</span>
          <span>{{article.CreatedAt}}</span>
        </div>
      </div>
      <ButtonGroup slot="extra" v-if="isAdmin">
        <article-tool :article="article"></article-tool>
      </ButtonGroup>

      <div class="article-content" >
        <div v-html="article.Content"></div>
      </div>

      <!-- pre article and next article -->
    </Card>
    <Card dis-hover>
      <div class="pre-next">
        <div v-if="pre" class="pre-article">
          <Icon type="md-arrow-round-back" />
          <a @click.prevent="toPreArticle">{{pre.Title}}</a>
        </div>
        <div v-if="next" class="next-article">
          <a @click.prevent="toNextArticle">{{next.Title}}</a>
          <Icon type="md-arrow-round-forward" />
        </div>
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
    validate ({ params }) {
      // 必须是number类型
      return /^\d+$/.test(params.id)
    },
    asyncData (ctx) {
      // console.log("article asyncData")
      // console.log("params:", ctx.params)
      // console.log("query:", ctx.query)

      return Promise.all([
        request.getArticleDetail({
          client: ctx.req,
          params: {
            id: ctx.params.id
          },
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
        let article = result.ad || {}
        let pre = result.pre
        let next = result.next

        return {
          article: article,
          pre: pre,
          next: next,
        }
      }).catch(err => {
        // console.log("catch error:", err)
        ctx.error({ message: "not found", statusCode: 404 })
      })
    },
    methods: {
      toPreArticle () {
        this.$router.push('/article/' + this.pre.ID)
      },
      toNextArticle () {
        this.$router.push('/article/' + this.next.ID)
      }
    },
    components: {
      "article-tool": ArticleTool,
    },
    layout: "nosidebar",
  }
</script>

<style lang="less" scoped>
  .article-title {
    /*font-size: 30px;*/
    /*font-weight: 700;*/
    margin-bottom: 10px;
    /*text-align: center;*/
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
    pre {
      margin: 5px;
      padding: 8px;
      background-color: #f6f6f6;
    }
  }
  .pre-next {
    overflow: auto;
  }
  .pre-article {
    float: left;
  }
  .next-article {
    float: right;
  }
</style>