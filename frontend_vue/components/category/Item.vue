<!-- 用于侧边栏 -->
<template>
  <div>
    <Button long type="default" class="cate-card-item" @click="toCatePage">
      <!-- todo: to category page -->
      <span class="cate-name">{{cate.Name}}</span>

      <div class="count-badge">
         <!--Badge, Tag, Button -->
         <!--type: success、primary、normal、error、warning、info	 -->
        <!-- todo: 该分类下的文章总数 -->
        <Badge type="normal" :count="cate.Count"></Badge>
      </div>

    </Button>
  </div>
</template>

<script>
  export default {
    props: ["cate"],
    data () {
      return {
        buttonSize: "small"
      }
    },
    methods: {
      toCatePage () {
        this.$router.push("/category/" + this.cate.ID)
      }
    },
  }
</script>

<style scoped>
  .cate-card-item {
    /*margin: 5px 8px;*/
    margin-bottom: 5px;
  }
  .cate-name{
    position: relative;
    display: inline-block;
    float: left;
    font-size: 14px;
  }
  .count-badge {
    margin-left: 10px;
    float: right;
  }
</style>