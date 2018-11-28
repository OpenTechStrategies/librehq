<template>
  <div v-if="messages" class="section">
    <div class="container">
      <div class="box">
        <div class="has-text-weight-bold">Messages</div>
        <ul v-for="message of messages" v-bind:key="message">
          <li>{{ message }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Messages"
};
</script>
