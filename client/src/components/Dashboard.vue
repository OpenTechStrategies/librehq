<template>
  <section class="section">
    <div class="container">
      <h1 class="title">Dashboard</h1>
      <section class="section">
        <div class="container">
          <div class="columns">
            <div class="column is-4">
              <div class="title">
                <a href="wikis/" class="is-size-4">Wikis</a>
              </div>
            </div>
            <div class="column is-4">
              <div class="title">Authorized Accounts</div>
              <div
                class="column is-4"
                v-for="account of accounts"
              >
                {{ account.username }}
              </div>
              <div>
                <label class="label">Authorize Account</label>
                <div class="control has-icons-left has-icons-right">
                  <input
                    class="input"
                    type="text"
                    v-model="username"
                    placeholder="Username or email"
                  >
                  <span class="icon is-small is-left">
                    <font-awesome-icon icon="user"></font-awesome-icon>
                  </span>
                </div>
                <input
                  class="button is-link"
                  type="submit"
                  value="Invite"
                  @click="inviteUser"
                >
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "Dashboard",
  data() {
    return {
      accounts: [],
      username: ""
    };
  },
  methods: {
    inviteUser() {
      axios
        .post("/addAuthorizedAccount", {
          usernameOrEmail: this.username
        })
      .then(res => {
        this.username = "";
        this.accounts = res.data;
      })
      .catch(error => {
        window.alert(error);
      });
    },
    getAuthorizedAccounts() {
      axios
        .get("/authorizedaccounts")
        .then(res => {
          this.accounts = res.data;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  created() {
    this.getAuthorizedAccounts();
  }
};
</script>
</script>
