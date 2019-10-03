<template>
  <div>
    <div class="tool-cell">
      <!--操作按钮-->
      <Card dis-hover v-if="isAdmin">
        <p slot="title" class="card-title">操作</p>
        <ButtonGroup>
          <Button :size="buttonSize" @click="toCreateArticle">
            <Icon type="md-create" />
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
          <Button :size="buttonSize" @click="toCateList"><Icon type="ios-code" /></Button>
          <Button :size="buttonSize" @click="toCreateCate"><Icon type="md-create" /></Button>
        </ButtonGroup>

        <cate-item
          v-for="cate in cates"
          v-if="cate.Count > 0"
          :cate="cate"
          :key="cate.ID"
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
  .tool-cell {
    /*padding: 8px;*/
  }
  .cate-cell {
    /*padding: 8px;*/
    /*padding-top: 8px;*/
  }
  .card-title {
    font-size: 16px;
    font-weight: bold;
  }
</style>