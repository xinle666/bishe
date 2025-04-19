// store/index.js
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        user: null // 或者 { id: '', role: '' }
    },
    mutations: {
        setUser(state, user) {
            state.user = user;
        }
    },
    actions: {
        login({ commit }, user) {
            // 登录逻辑
            commit('setUser', user);
        },
        logout({ commit }) {
            // 登出逻辑
            commit('setUser', null);
        }
    }
});
