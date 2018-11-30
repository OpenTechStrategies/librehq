import Vue from "vue";
import App from "../../App.vue";
import Account from "../../components/Account.vue";

Vue.config.productionTip = false;

new Vue({
  render: createElement =>
    createElement(App, { props: { loggedIn: true } }, [createElement(Account)])
}).$mount("#app");
