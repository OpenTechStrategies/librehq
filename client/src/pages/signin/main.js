import Vue from "vue";
import App from "../../App.vue";
import Signin from "../../components/Signin.vue";

Vue.config.productionTip = false;

new Vue({
  render: createElement =>
    createElement(App, { props: { loggedIn: false } }, [createElement(Signin)])
}).$mount("#app");
