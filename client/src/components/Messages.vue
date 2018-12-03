<template>
  <div v-if="messages.length" class="section">
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
import axios from "axios";

export default {
  name: "Messages",
  data() {
    return {
      messages: []
    };
  },
  methods: {
    getMessages() {
      axios
        .get("/getmessages")
        .then(res => {
          this.messages = res.data;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  created() {
    this.getMessages();
  }
};
</script>
