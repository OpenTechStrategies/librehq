<template>
  <div>
    <section class="section">
      <div class="container">
        <h1 class="title">My Account {{
          account.username ? "(" + account.username + ")" : ""
        }}</h1>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="columns">
          <div class="column is-one-third">
            <h2 class="title is-4">Update Account</h2>
            <form action="updateAccount" method="post">

              <div class="field">
                <label class="label">Change Username</label>
                <div class="control has-icons-left has-icons-right">
                  <input
                    class="input"
                    type="text"
                    name="username"
                    placeholder="Username"
                    v-bind:value="account.username"
                  >
                  <span class="icon is-small is-left">
                    <font-awesome-icon icon="user"></font-awesome-icon>
                  </span>
                </div>
              </div>

              <div class="field">
                <label class="label">Change Password</label>
                <div class="control has-icons-left has-icons-right">
                  <input
                    class="input"
                    type="password"
                    name="password"
                    placeholder="Password"
                  >
                  <span class="icon is-small is-left">
                    <font-awesome-icon icon="key"></font-awesome-icon>
                  </span>
                </div>
              </div>

              <div class="field">
                <label class="label">Change Email Address</label>
                <div class="control has-icons-left has-icons-right">
                  <input
                    class="input"
                    type="email"
                    name="email"
                    placeholder="Email Address"
                    v-bind:value="account.email"
                  >
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
                    value="Update Account"
                  >
                </div>
              </div>

            </form>
          </div>
          <div class="column">

            <h2 class="title is-4">Delete Account</h2>
            <form action="deleteAccount" method="post">
              <input
                class="button is-danger"
                type="submit"
                onclick="return window.confirm('Confirm Delete Account')"
                value="Delete Account"
              >
            </form>

          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Account",
  data() {
    return {
      account: {
        username: "",
        email: ""
      }
    };
  },
  methods: {
    getAccountData() {
      axios
        .get("/account-data")
        .then(res => {
          this.account = res.data.account;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  created() {
    this.getAccountData();
  }
};
</script>
