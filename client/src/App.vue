<template>
  <div id="app">
    <Header v-bind:loggedIn="page === 'dashboard' || page === 'account'"/>
    <Messages />
    <Signin v-if="page === 'signin'"/>
    <Dashboard v-else-if="page === 'dashboard'"/>
    <Account v-else-if="page === 'account'"/>
    <Footer />
  </div>
</template>

<script>
import "./assets/sass/main.scss";
import "./fontawesome.js";
import Header from "./components/Header.vue";
import Messages from "./components/Messages.vue";
import Signin from "./components/Signin.vue";
import Dashboard from "./components/Dashboard.vue";
import Account from "./components/Account.vue";
import Footer from "./components/Footer.vue";

export default {
  name: "app",
  components: {
    Header,
    Messages,
    Signin,
    Dashboard,
    Account,
    Footer
  },
  props: {
    page: String
  }
};
</script>

<!-- <style lang="scss"></style> -->
