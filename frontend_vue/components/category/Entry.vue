<template>
  <div>
    <Card>
      {{cate.Name}}
      <ButtonGroup class="cate-tool">
        <Button :size="buttonSize" @click="toEditPage"><Icon type="ios-code" /></Button>
        <Button :size="buttonSize" @click="deleteConfirm = true"><Icon type="ios-close" /></Button>
        <Modal
          v-model="deleteConfirm"
          title="delete or not ?"
          @on-ok="deleteCategory"
        >
          <p>delete category</p>
        </Modal>
      </ButtonGroup>
    </Card>
  </div>
</template>

<script>
  import request from '~/api/request'

  export default {
    props: ["cate"],
    data () {
      return {
        buttonSize: "small",
        edit: false,
        deleteConfirm: false,
      }
    },
    methods: {
      toEditPage () {
        this.$router.push("/category/update/" + this.cate.ID)
      },
      deleteCategory () {
        // console.log('delete category')
        // console.log(this.$router.history.current)
        let self = this
        request.deleteCate({
          params: {
            id: this.cate.ID,
          }
        }).then(resp => {
          if (resp.code === 0) {
            this.$Message.info("delete category success")
            this.$router.push('/')
          } else {
            this.$Message.error({
              duration: 3,
              closable: true,
              content: resp.message || resp.msg,
            })
          }
        }).catch(err => {
          this.$Message.error({
            duration: 3,
            closable: true,
            content: err.message || err.msg,
          })
        })
      },
    },
  }
</script>

<style scoped>
  .cate-tool {
    float: right;
  }
</style>
