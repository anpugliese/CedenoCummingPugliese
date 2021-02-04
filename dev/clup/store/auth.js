export const state = () => ({
    auth: false
  })
  
  export const mutations = {
    updateAuth(state,auth) {
      state.auth = auth
    }
  }

  export const actions = {
    login({ commit }, payload ){
        window.localStorage.setItem("access_token", payload);
        commit("updateAuth", true);
    },
    logout({commit}, payload){
        window.localStorage.clear();
        commit("updateAuth", false);
    },
    getToken({commit}){
        return window.localStorage.getItem("access_token");
    }
  }