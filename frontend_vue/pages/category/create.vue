<template>
  <div>
    <cate-editor
      :cate="cate"
    >
    </cate-editor>
  </div>
</template>

<script>
  import CateEditor from "~/components/category/Editor"

  export default {
    data () {
      return {
        cate: null,
      }
    },
    components: {
      "cate-editor": CateEditor,
    },
    layout: "nosidebar",
    middleware: "loginRequired"
  }
</script>
