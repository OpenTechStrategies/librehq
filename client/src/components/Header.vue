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
            <a v-if="loggedIn"
              role="button"
              class="navbar-burger burger"
              aria-label="menu"
              aria-expanded="false"
            >
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
            </a>
        </div>

        <div
          v-if="loggedIn"
          id="mainNavbar"
          class="navbar-menu"
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
    loggedIn: Boolean
  }
};
</script>
