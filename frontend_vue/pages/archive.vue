<template>
  <div>
    <year-line
      v-for="artOfTheYear in artListByYear"
      :artOfTheYear="artOfTheYear"
      :key="artOfTheYear.year"
    >
    </year-line>
  </div>
</template>

<script>
  import request from '~/api/request'
  import YearLine from '~/components/archive/YearLine'

  export default {
    data () {
      return {}
    },
    asyncData (ctx) {
      // console.log("index asyncData")
      return Promise.all([
        request.getArchive({
          client: ctx.req
        }),
      ]).then(resp => {
        // console.log("get data:", resp)

        // categories
        let artListByYear = resp[0].data.al || {}
        return {
          artListByYear: artListByYear,
        }
      }).catch(err => {
        console.log("catch error:", err)
        ctx.error({ message: "not found", statusCode: 404 })
      })
    },
    methods: {},
    layout: 'default',
    components: {
      "year-line": YearLine,
    }
  }
</script>