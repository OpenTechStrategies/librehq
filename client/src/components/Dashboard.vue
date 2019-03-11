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
      accounts: []
    };
  },
  methods: {
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
