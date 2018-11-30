import Vue from "vue";
import App from "../../App.vue";
import Dashboard from "../../components/Dashboard.vue";

Vue.config.productionTip = false;

new Vue({
  render: createElement =>
    createElement(App, { props: { loggedIn: true } }, [
      createElement(Dashboard)
    ])
}).$mount("#app");
