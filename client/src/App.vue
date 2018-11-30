<template>
  <div id="app">
    <Header v-bind:loggedIn="loggedIn"/>
    <Messages />
    <slot />
    <Footer />
  </div>
</template>

<script>
import "./assets/sass/main.scss";
import "./fontawesome.js";
import Header from "./components/Header.vue";
import Messages from "./components/Messages.vue";
import Footer from "./components/Footer.vue";

export default {
  name: "app",
  components: {
    Header,
    Messages,
    Footer
  },
  props: {
    loggedIn: Boolean
  }
};
</script>

<!-- <style lang="scss"></style> -->
