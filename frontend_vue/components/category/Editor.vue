<template>
  <div>
    <Form ref="formData" :model="formData" :rules="validRules">
      <FormItem label="name" prop="name">
        <Input v-model="formData.name" placeholder="Enter a name"></Input>
      </FormItem>
      <FormItem>
        <Button type="primary" @click="saveCate('formData')">Submit</Button>
      </FormItem>
    </Form>
  </div>
</template>

<script>
  import request from '~/api/request'

  export default {
    props: ['cate'],
    data () {
      return {
        formData: {
          name: (this.cate && this.cate.Name) || ''
        },
        validRules: {
          name: [
            { required: true, type:"string", min:3, max:20, trigger: "blur"},
          ],
        }
      }
    },
    methods: {
      saveCate (name) {
        // console.log("save category")
        let self = this
        this.$refs[name].validate((valid) => {
          if (!valid) {
            this.$Message.error('input error');
            console.log("input not valid:", this.formData)
            return
          }

          // 如果有cate，表示是更新分类，否则是新建分类
          let sendReq = this.cate ? request.updateCate : request.createCate
          let params = this.cate ? { id: this.cate.ID } : null
          let body = {
            name: this.formData.name,
          }
          // 发送请求
          sendReq({
            params: params,
            body: body
          }).then(resp => {
            // console.log(resp)
            if (resp.code === 0) {
              let cate = resp.data.cate
              this.$Message.info("update cate success")
              // 成功后跳转到分类列表页
              this.$router.push('/category/list')
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
        })
      }
    },
    middleware: "loginRequired",
  }
</script>