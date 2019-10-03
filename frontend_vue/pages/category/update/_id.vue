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
  import request from '~/api/request'

  export default {
    data () {
      return {}
    },
    validate ({ params }) {
      // 必须是number类型
      return /^\d+$/.test(params.id)
    },
    asyncData (ctx) {
      // console.log("article asyncData")
      // console.log("params:", ctx.params)

      return Promise.all([
        request.getCateDetail({
          client: ctx.req,
          params: {
            id: ctx.params.id
          }
        })
      ]).then(resp => {
        // console.log("get data:", resp)
        let cate = resp[0].data.cate || null

        return {
          cate: cate
        }
      }).catch(err => {
        console.log("catch error:", err)
        ctx.error({ message: "not found", statusCode: 404 })
      })
    },
    components: {
      "cate-editor": CateEditor,
    },
    layout: "nosidebar",
    middleware: "loginRequired"
  }
</script>
