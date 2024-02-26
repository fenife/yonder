<template>
  <div class="app-header">
    <Menu mode="horizontal" :theme="menu_theme" @on-select="navRoute">
      <div class="app-logo">
        <a href="/">Yonder</a>
      </div>
      <!--<div class="app-header-left">-->
      <div>
        <MenuItem name="home">首页</MenuItem>
        <MenuItem name="archive" >归档</MenuItem>
        <MenuItem name="about">关于</MenuItem>
      </div>

      <div class="app-header-search">
        <!--<Input suffix="ios-search" placeholder="search"/>-->
        <Input search placeholder="搜索 ... " v-model="searchValue" @on-search="handleSearch"/>
      </div>

<!--      <div class="app-header-right">-->
<!--        <div v-if="user">-->
<!--          <MenuItem name="signout">退出</MenuItem>-->
<!--        </div>-->
<!--        <div v-else>-->
<!--          <MenuItem name="signin">登陆</MenuItem>-->
<!--          <MenuItem name="signup">注册</MenuItem>-->
<!--        </div>-->
<!--      </div>-->

    </Menu>
  </div>
</template>

<script>
  import request from '~/api/request'

  export default {
    data () {
      return {
        user: this.$store.state.user,
        menu_theme: 'light',
        searchValue: ""
      }
    },
    methods: {
      navRoute (name) {
        switch (name) {
          case 'home':
            this.$router.push("/")
            break
          case 'archive':
            this.$router.push("/archive")
            break
          case 'about':
            this.$router.push("/about")
            break
          case 'signup':
            this.$router.push("/signup")
            break
          case 'signin':
            this.$router.push("/signin")
            break
          case 'signout':
            this.onSignout()
            break
          default:
            // todo: page not found
            console.log("page not found")
        }
      },
      handleSearch () {
        // console.log("searchValue:", this.searchValue)
        if (this.searchValue) {
          this.$router.push("/search/" + this.searchValue)
          this.searchValue = ''
        } else {
          this.$Message.warning("搜索内容不能为空")
        }
      },
      onSignout () {
        request.signout()
          .then(resp => {
            if (resp.code === 0) {
              this.$store.commit('setUser', null)
              this.$Message.info({
                duration: 3,
                closable: true,
                content: "登陆成功"
              })
              // fresh user state and reload page
              window.location.href = '/'
            } else {
              this.$Message.info(resp.msg)
            }
          })
          .catch(err => {
            this.$Message.error({
              duration: 3,
              closable: true,
              content: err.message || err.msg,
            })
          })
      },
    }
  }
</script>

<style scoped>
  .app-header {
    position: relative;
    overflow: hidden;
  }
  .app-logo {
    position: relative;
    float: left;
    color: rgba(255,255,255,.7);
    font-size: 20px;
    font-weight: bold;
    padding: 0 40px;
  }
  .app-header-search{
    position: relative;
    float: left;
    /*position: center;*/
    padding: 0 20px;
  }
  .app-header-right {
    margin: 0 auto;
    float: right;
    margin-right: 20px;
  }
</style>