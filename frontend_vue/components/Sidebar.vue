<template>
  <div>
    <div class="person-info">
      <Card dis-hover>
        <p slot="title" class="card-title">个人空间</p>

        <Tooltip content="源码" placement="bottom" theme="light">
          <a class="person-info-item" href="https://github.com/fenife/yonder.git">
            <Icon size="30" type="logo-github" />
          </a>
        </Tooltip>

        <Poptip trigger="hover" title="邮箱联系" content="fenife@163.com" placement="top">
          <Icon class="person-info-item" size="30" type="md-mail" />
        </Poptip>

      </Card>
    </div>

    <div v-if="isAdmin" class="tool-cell">
      <!--操作按钮-->
      <Card dis-hover>
        <p slot="title" class="card-title">文章操作</p>
        <ButtonGroup>
          <Button :size="buttonSize" @click="toCreateArticle">
<!--            <Icon type="md-create" />-->
            <Icon type="md-add" />
          </Button>
          <Button :size="buttonSize" @click="toTrashPage">
            <!--<Icon type="md-create" />-->
            <Icon type="ios-trash-outline" />
          </Button>
        </ButtonGroup>
      </Card>
    </div>

    <div class="cate-cell">
      <Card dis-hover>
        <p slot="title" class="card-title">文章分类</p>
        <ButtonGroup slot="extra" v-if="isAdmin">
          <Button :size="buttonSize" @click="toCateList"><Icon type="md-list" /></Button>
          <Button :size="buttonSize" @click="toCreateCate"><Icon type="md-add" /></Button>
        </ButtonGroup>

        <cate-item
          v-for="cate in cates"
          v-if="cate.post_count > 0"
          :cate="cate"
          :key="cate.id"
        >
        </cate-item>
      </Card>
    </div>
  </div>
</template>

<script>
  import CateItem from '~/components/category/Item'

  export default {
    data () {
      return {
        cates: this.$store.state.cates || [],
        isAdmin: this.$store.state.isAdmin || false,
        buttonSize: "small"
      }
    },
    methods: {
      toCreateArticle () {
        this.$router.push("/article/create")
      },
      toTrashPage () {
        // todo: to trash page
        console.log('to trash page')
      },
      toCateList () {
        this.$router.push("/category/list")
      },
      toCreateCate () {
        this.$router.push("/category/create")
      }
    },
    components: {
      'cate-item': CateItem
    }
  }
</script>

<style scoped>
  .person-info a {
    color: inherit;
  }
  .person-info-item {
    /*padding-left: 5px;*/
    padding-right: 15px;
    /*margin-right: 15px;*/
  }

  .tool-cell {
    /*padding: 8px;*/
    padding-top: 8px;
  }
  .cate-cell {
    /*padding: 8px;*/
    padding-top: 8px;
  }
  .card-title {
    font-size: 16px;
    font-weight: bold;
  }
</style>