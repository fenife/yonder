<template>
  <div class="article-cell">
    <Card :bordered="false">
      <a slot="title" class="article-title"  @click.prevent="toDetailPage">
        {{article.title}}
      </a>
      <!--todo: edit article-->
      <!--<div slot="extra" v-if="isAdmin">-->
        <!--<article-tool :article="article"></article-tool>-->
      <!--</div>-->

      <div class="card-body">
        <Button :size="buttonSize" type="text">{{article.user.name}}</Button>
        <Button :size="buttonSize" type="text">{{article.created_at}}</Button>
        <!-- <Button :size="buttonSize" type="text">{{article.updated_at}}</Button> -->
        <!-- todo: to category page -->
        <Button :size="buttonSize" type="info" shape="circle" :ghost="true" @click="toCatePage">
          {{article.category.name}}
        </Button>

      </div>
    </Card>
  </div>
</template>

<script>
  import ArticleTool from '~/components/article/Tool'

  export default {
    props: ['article'],
    data () {
      return {
        buttonSize: "small",
        isAdmin: this.$store.state.isAdmin || false,
      }
    },
    methods: {
      toDetailPage () {
        this.$router.push("/article/" + this.article.id)
      },
      toCatePage () {
        this.$router.push("/category/" + this.article.cate_id)
      },
    },
    components: {
      "article-tool": ArticleTool,
    }
  }
</script>

<style scoped>
  .article-cell {
    padding-bottom: 8px;
  }
  .article-title {
    font-size: 20px;
  }
</style>