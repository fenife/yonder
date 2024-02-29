<template>
  <div class="year-cell">
    <Card>
      <p slot="title" class="card-title">{{artOfTheYear.year}} 年（{{artOfTheYear.count}} 篇）</p>
      <Timeline>
        <TimelineItem v-for="art in artOfTheYear.post_list" :key="art.id" class="time-item">
          <span class="time">{{art.created_at}}</span>
          <a class="content" @click="toArticle(art.id)">{{art.title}}</a>
        </TimelineItem>
      </Timeline>
    </Card>
  </div>
</template>

<script>
  export default {
    props: ["artOfTheYear"],
    methods: {
      toArticle (artId) {
        this.$router.push('/article/' + artId)
      }
    }
  }
</script>

<style scoped>
  .year-cell {
    padding-bottom: 8px;
  }
  .card-title {
    font-size: 20px;
  }
  .time {
    font-size: 17px;
  }
  .content {
    font-size: 17px;
    padding-left: 5px;
  }
  .time-item {
    padding: 0;
  }
</style>