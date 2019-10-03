<template>
  <div class="app-body">
    <app-header />
    <div class="app-container">
      <!-- 间隔32px -->
      <Row :gutter="16">
        <!--<Col span="3">a</Col>-->
        <Col span="16">
          <nuxt />
        </Col>
        <Col span="8">
          <app-sidebar />
        </Col>
        <!--<Col span="3">a</Col>-->
      </Row>
    </div>
  </div>
</template>

<script>
  import Header from '~/components/Header'
  import Sidebar from '~/components/Sidebar'

  export default {
    components: {
      'app-header': Header,
      'app-sidebar': Sidebar
    }
  }
</script>

<style scoped>
  .app-body {
    background:#eee;
    padding-bottom: 8px;
  }
  .app-container {
    width: 1080px;
    margin: 8px auto;
    min-height: 400px;
  }
</style>
