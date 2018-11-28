import { library } from "@fortawesome/fontawesome-svg-core";
import { faUser, faEnvelope, faKey } from "@fortawesome/free-solid-svg-icons";
library.add(faUser, faEnvelope, faKey);

import Vue from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
Vue.component("font-awesome-icon", FontAwesomeIcon);
