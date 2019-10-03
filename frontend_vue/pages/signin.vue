<template>
  <div>
    <Form ref="info" :model="info" :rules="validRules" class="login">
      <FormItem label="Name" prop="username">
        <Input v-model="info.username" placeholder="Enter your name"></Input>
      </FormItem>
      <FormItem label="Password" prop="passwd">
        <Input type="password" v-model="info.passwd" placeholder="Enter your password"></Input>
      </FormItem>
      <FormItem>
        <Button type="primary" @click="login('info')">Submit</Button>
      </FormItem>
    </Form>
  </div>
</template>

<script>
  import request from '~/api/request'

  export default {
    data () {
      return {
        info: {
          username: '',
          passwd: '',
        },
        validRules: {
          username: [
            { required: true, type:"string", min:4, max: 20, trigger: "blur"},
          ],
          passwd: [
            { required: true, type:"string", min:3, max: 20, trigger: "blur"},
          ]
        }
      }
    },
    methods: {
      login (name) {
        let self = this
        this.$refs[name].validate((valid) => {
          if (!valid) {
            this.$Message.error('input error');
            // console.log("input not valid:", this.info)
            return
          }

          request.signin({
            body: {
              name: this.info.username,
              password: this.info.passwd,
            }
          }).then(resp => {
              console.log("resp:", resp)
              if (resp.code === 0) {
                // sigin success
                this.$Message.info("signin success")
                self.$store.commit("setToken", resp.data.token)
                self.$store.commit("setUser", resp.data.user)
                this.$router.push('/')
              } else {
                this.$Message.error({
                  duration: 3,
                  closable: true,
                  content: resp.message || resp.msg,
                  })
              }
            }
          ).catch(
            this.$Message.error({
              duration: 3,
              closable: true,
              content: err.message || err.msg,
            })
          )
        })
      }
    },
    layout: "nosidebar"
  }
</script>

<style scoped>
  .login {
    width: 300px
  }
</style>
