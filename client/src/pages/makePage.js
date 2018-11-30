import Vue from "vue";
import App from "../App.vue";

Vue.config.productionTip = false;

export default (appProps, childComponent) =>
  new Vue({
    render: createElement =>
      createElement(App, { props: appProps }, [createElement(childComponent)])
  }).$mount("#app");
