<template>
  <div id="app">
    <Header v-bind:signedIn="signedIn"/>
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
    signedIn: Boolean
  }
};
</script>

<!-- <style lang="scss"></style> -->
