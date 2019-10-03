<template>
  <div>
    <Form ref="formData" :model="formData" :rules="validRules">
      <FormItem label="title" prop="title">
        <Input v-model="formData.title" placeholder="Enter a title"></Input>
      </FormItem>
      <FormItem label="category" prop="cate">
        <Select v-model="formData.cateId" placeholder="select a category">
          <Option
            v-for="cate in cates"
            :value="cate.ID"
            :key="cate.ID"
          >
            {{cate.Name}}
          </Option>
        </Select>
      </FormItem>
      <FormItem prop="content">
        <!--<Input type="textarea" v-model="formData.content" placeholder="content"></Input>-->
        <div>
          <md-editor
            :value="formData.content"
            v-model="formData.content"
          >
          </md-editor>
        </div>
      </FormItem>
      <FormItem>
        <Button type="primary" @click="saveArticle('formData')">Submit</Button>
      </FormItem>
    </Form>
  </div>
</template>

<script>
  import MarkdownEditor from '~/components/markdown'
  import request from '~/api/request'

  export default {
    props: [
      "user",
      "article",
      "cates",
    ],
    data () {
      return {
        formData: {
          title: (this.article && this.article.Title) || '',
          cateId: (this.article && this.article.Category.ID) || '',
          content: (this.article && this.article.Content) || '',
        },
        validRules: {
          title: [
            { required: true, type:"string", trigger: "blur"},
          ],
          cateId: [
            { required: true, type: "number"},
          ],
          content: [
            { required: true, type:"string", trigger: "blur"},
          ]
        }
      }
    },
    methods: {
      saveArticle (name) {
        let self = this
        this.$refs[name].validate((valid) => {
          if (!valid) {
            this.$Message.error('input error');
            console.log("input not valid:", this.formData)
            return
          }

          // 如果有article，表示是更新文章，否则是新建文章
          let sendReq = this.article ? request.updateArticle : request.createArticle
          let params = this.article ? { id: this.article.ID } : null
          let body = {
            title: this.formData.title,
            cateId: this.formData.cateId,
            content: this.formData.content,
          }
          // 发送请求
          sendReq({
            params: params,
            body: body
          }).then(resp => {
            // console.log(resp)
            if (resp.code === 0) {
              let article = resp.data.ad
              this.$Message.info("update article success")
              // 成功后跳转到文章详情页
              this.$router.push('/article/' + article.ID)
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
      },
    },
    components: {
      "md-editor": MarkdownEditor,
    },
    middleware: "loginRequired",
  }
</script>