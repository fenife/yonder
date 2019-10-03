<template>
  <div class="year-cell">
    <Card>
      <p slot="title" class="card-title">{{artOfTheYear.Year}} 年</p>
      <Timeline>
        <TimelineItem v-for="art in artOfTheYear.ArtList" :key="art.ID" class="time-item">
          <span class="time">{{art.CreatedAt}}</span>
          <a class="content" @click="toArticle(art.ID)">{{art.Title}}</a>
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
    font-size: 18px;
  }
  .time {
    font-size: 16px;
  }
  .content {
    font-size: 16px;
  }
  .time-item {
    padding: 0;
  }
</style>