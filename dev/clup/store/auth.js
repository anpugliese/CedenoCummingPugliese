export const state = () => ({
    auth: false,
    username: '',
  })
  
  export const mutations = {
    updateAuth(state,auth) {
      state.auth = auth
    },
    updateUsername(state, username){
        state.username = username
    }
  }

  export const actions = {
    login({ commit }, payload, username ){
        window.localStorage.setItem("access_token", payload);
        commit("updateAuth", true);
        commit("updateUsername", username);
    },
    logout({commit}, payload){
        window.localStorage.clear();
        commit("updateAuth", false);
        commit("updateUsername", '');
    },
    getToken({commit}){
        return window.localStorage.getItem("access_token");
    },
    
  }

  export const getters = {
      getAuthState(state){
        return state.auth;
      },
      getUsername(state){
        return state.username;
      }
  }