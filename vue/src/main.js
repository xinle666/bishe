import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import './assets/allCss.css'
import VueRouter from "vue-router"; //路由
import router from "@/router/main";
import axios from 'axios';




Vue.use(VueRouter);
Vue.use(ElementUI);
Vue.config.productionTip = false
Vue.prototype.$axios =axios;
Vue.prototype.$eventBus = new Vue();
Vue.prototype.$httpUrl = "http://127.0.0.1:8000";
new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
