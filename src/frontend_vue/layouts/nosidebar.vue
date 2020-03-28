<template>
  <div class="app-body">
    <app-header />
    <div class="app-container">
      <nuxt />
    </div>
  </div>
</template>

<script>
  import Header from '~/components/Header'

  export default {
    components: {
      'app-header': Header,
    }
  }
</script>

<style scoped>
  .app-body {
    background:#eee;
    padding-bottom: 8px;
  }
  .app-container {
    background:#eee;
    width: 1080px;
    margin: 8px auto;
    min-height: 300px;
  }
</style>
