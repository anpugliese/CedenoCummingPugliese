export const state = () => ({
    selected_supermarket: '',
    supermarket_list: [],
  })
  
  export const mutations = {
    updateSelectedSupermarket(state,selected_supermarket) {
        state.selected_supermarket = selected_supermarket
    },
    updateSupermarketList(state, supermarket_list){
        state.supermarket_list = supermarket_list
    }
  }

  export const actions = {
    setSelectedSupermarket({commit}, selected){
        commit("updateSelectedSupermarket", selected);
    },

    setSupermarketList({commit}, supermarketList){
        commit("updateSupermarketList", supermarketList);
    },
    
  }
  
  export const getters = {
      getSelectedSupermarket(state){
        return state.selected_supermarket;
      },
      getSupermarketList(state){
        return state.supermarket_list;
      }
  }