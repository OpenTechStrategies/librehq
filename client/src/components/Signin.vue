<template>
  <section class="section">
    <div class="container">
      <div class="columns">

        <div class="column">
          <h1 class="title">
            LibreHQ <em>beta</em>
          </h1>
          <p class="subtitle">
            This is the subtitle.
          </p>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
            ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
            aliquip ex ea commodo consequat.
          </p>
        </div>

        <div class="column"></div>

        <div class="column">
          <div class="tabs is-large is-boxed is-fullwidth">
            <ul>
              <li v-bind:class="signUp && 'is-active'">
                <a @click="showSignUp">Sign Up</a>
              </li>
              <li v-bind:class="!signUp && 'is-active'">
                <a @click="showSignIn">Sign In</a>
              </li>
            </ul>
          </div>

          <form
            v-bind:action="signUp ? 'signup' : 'signin'"
            method="post"
          >
            <div class="field">
              <label class="label">Username</label>
              <div class="control has-icons-left has-icons-right">
                <input class="input" type="text" name="username" placeholder="Username">
                <span class="icon is-small is-left">
                  <font-awesome-icon icon="user"></font-awesome-icon>
                </span>
              </div>
            </div>

            <div class="field">
              <label class="label">Password</label>
              <div class="control has-icons-left has-icons-right">
                <input class="input" type="password" name="password" placeholder="Password">
                <span class="icon is-small is-left">
                  <font-awesome-icon icon="key"></font-awesome-icon>
                </span>
              </div>
            </div>

            <div
              class="field"
              v-if="signUp"
            >
              <label class="label">Email</label>
              <div class="control has-icons-left has-icons-right">
                <input class="input" type="email" name="email" placeholder="Email Address">
                <span class="icon is-small is-left">
                  <font-awesome-icon icon="envelope"></font-awesome-icon>
                </span>
              </div>
            </div>

            <div class="field">
              <div class="control">
                <input
                  class="button is-link"
                  type="submit"
                  v-bind:value="signUp ? 'Sign Up' : 'Sign In'"
                >
              </div>
            </div>

          </form>
        </div>

      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "Signin",
  data() {
    return {
      signUp: true
    };
  },
  methods: {
    showSignUp() {
      this.signUp = true;
    },
    showSignIn() {
      this.signUp = false;
    }
  }
};
</script>
