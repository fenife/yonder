<template>
  <div>
    <h1>category list</h1>
    <cate-entry
      v-for="cate in cates"
      :cate = cate
      :key="cate.ID"
    >
    </cate-entry>
  </div>
</template>

<script>
  import CateEntry from '~/components/category/Entry'
  import request from '~/api/request'

  export default {
    asyncData (ctx) {
      // console.log("index asyncData")
      return Promise.all([
        request.getCates({
          client: ctx.req
        })
      ]).then(resp => {
        // console.log("get data:", resp)

        // categories
        let cates = resp[0].data.cateList || []
        // console.log("cates", cates)
        // ctx.store.commit('setCates', cates)

        return {
          cates: cates
        }
      }).catch(err => {
        console.log("catch error:", err)
        ctx.error({ message: "not found", statusCode: 404 })
      })
    },
    components: {
      "cate-entry": CateEntry,
    },
    middleware: "loginRequired",
  }
</script>
