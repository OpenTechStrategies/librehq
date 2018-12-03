<template>
  <div class="container">
    <header>
      <nav
        class="navbar is-primary"
        role="navigation"
        aria-label="main navigation"
      >

        <div class="navbar-brand">
          <a
            class="navbar-item has-text-weight-bold"
            href="/"
          >LibreHQ <em>beta</em></a>
            <a v-if="signedIn"
              role="button"
              class="navbar-burger burger"
              v-bind:class="mainNavActive"
              aria-label="menu"
              aria-expanded="false"
              @click="toggleMainNavActive"
            >
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
            </a>
        </div>

        <div
          v-if="signedIn"
          id="mainNavbar"
          class="navbar-menu"
          v-bind:class="mainNavActive"
        >

          <div class="navbar-start">
            <a class="navbar-item" href="/">
              Dashboard
            </a>
            <a class="navbar-item" href="/account">
              My Account
            </a>
          </div>

          <div class="navbar-end">
            <a class="navbar-item" href="/signout">
              Sign Out
            </a>
          </div>

        </div>

      </nav>
    </header>
  </div>
</template>

<script>
export default {
  name: "Header",
  props: {
    signedIn: Boolean
  },
  data() {
    return {
      mainNavActive: {
        "is-active": false
      }
    };
  },
  methods: {
    toggleMainNavActive() {
      this.mainNavActive["is-active"] = !this.mainNavActive["is-active"];
    }
  }
};
</script>
