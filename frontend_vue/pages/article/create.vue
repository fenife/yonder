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

  export default {
    data () {
      return {
        user: this.$store.state.user,
        cates: this.$store.state.cates,
        article: null,
      }
    },
    components: {
      "article-editor": ArticleEditor,
    },
    layout: "nosidebar",
    middleware: "loginRequired"
  }
</script>
