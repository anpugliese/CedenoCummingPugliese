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
    login({ commit }, payload ){
        window.localStorage.setItem("access_token", payload.token);
        window.localStorage.setItem("username", payload.username);
        commit("updateAuth", true);
        commit("updateUsername", payload.username);
    },
<<<<<<< HEAD
    logout({commit}, payload){
=======
    logout({commit}){
>>>>>>> main
        window.localStorage.clear();
        commit("updateAuth", false);
        commit("updateUsername", '');
    },
    getToken({commit}){
        return window.localStorage.getItem("access_token");
    },
    getUsername({commit}){
        return window.localStorage.getItem("username");
    },
<<<<<<< HEAD
=======
    isLoggedIn({commit}){
      return window.localStorage.getItem("username") != null;
    }
>>>>>>> main
    
  }

  export const getters = {
      getAuthState(state){
        return state.auth;
      },
      getUsername(state){
        return state.username;
      }
  }