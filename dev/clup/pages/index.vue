<template>
  <div>
    <div class="overlay" @click="hidePopup()" v-if="display_popup">
      <div class="popup">
        <h4>{{ popup_message }}</h4>
      </div>
    </div>
    <!-- Button bar in the three bottom left  -->
    <div class="button-bar">
      <div class="round-button" v-on:click="filterIsActive = !filterIsActive">
        <fa-icon :icon="['fas', 'filter']" class="round-button-icon" />
      </div>

      <div class="filter-popup" id="filter-form" v-if="filterIsActive">
        <h5 style="text-align: center; padding-top: 5px">Filters</h5>
        <div class="slidecontainer">
          <input
            type="range"
            min="1"
            max="100"
            value="50"
            v-model="slider_value"
          />
          <h6>Waiting time less than {{ slider_value }} minutes</h6>
        </div>
        <div class="check" v-for="sp in supermarkets_names" :key="sp.id">
          <label :for="sp.id">
            <input type="checkbox" v-model="sp.active" :name="sp.id" />
            {{ sp.name }} </label
          ><br />
        </div>
        <div style="text-align: center">
          <button @click="applyFilter()" type="submit">Apply</button>

          <button @click="clearFilter()" style="background: red" type="submit">
            Clear
          </button>
        </div>
      </div>

      <div class="round-button">
        <NuxtLink to="/list">
          <fa-icon :icon="['fas', 'running']" class="round-button-icon" />
        </NuxtLink>
      </div>

      <div class="round-button">
        <NuxtLink to="/qrcode">
          <fa-icon :icon="['fas', 'qrcode']" class="round-button-icon" />
        </NuxtLink>
      </div>
    </div>

    <div class="round-logout-button" @click="logout()">
      <div>
        <fa-icon
          :icon="['fas', 'sign-out-alt']"
          class="round-logout-button-icon"
        />
      </div>
    </div>

    <!-- Search bar (non functional yet)
  <div class="wrap">
   <div class="search">
        <input type="text" class="searchTerm" placeholder="Search for a supermarket">
        <button type="submit" class="searchButton">
          <fa-icon :icon="['fas', 'search']" />
        </button>
    </div>
  </div>
  -->

    <!-- Render leaflet map -->
    <div class="map-container">
      <div id="map-wrap" style="height: 100%; width: 100%">
        <client-only>
          <l-map :zoom="15" :center="[map_lat, map_lng]" :options="map_options">
            <l-tile-layer
              url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
            ></l-tile-layer>
            <l-marker :lat-lng="[map_lat, map_lng]" :icon="icon"> </l-marker>

            <!-- Iterate to render nearby supermarkets markers -->
            <l-marker
              v-for="supermarket in new_supermarkets_list"
              :key="supermarket.id"
              :lat-lng="[supermarket.lat, supermarket.lon]"
              :icon="icon"
            >
              <l-icon :icon-anchor="staticAnchor" class-name="someExtraClass">
                <div
                  class="supermarket-card"
                  style="margin: 2px"
                  :class="{
                    'red-marker': supermarket.waiting_time >= 15,
                    'yellow-marker':
                      supermarket.waiting_time < 15 &&
                      supermarket.waiting_time >= 5,
                    'green-marker': supermarket.waiting_time < 5,
                  }"
                >
                  <div style="background-color: white">
                    <img width="50" v-bind:src="supermarket.logo" />
                  </div>
                  <span class="waiting-time">{{ supermarket.name }}</span>
                  <span class="waiting-time"
                    >{{ supermarket.waiting_time }} MINS</span
                  >
                </div>
              </l-icon>
              <l-popup>
                <div style="width: 150px; padding: 0">
                  <h6 class="popup-title">{{ supermarket.name }}</h6>
                  <div class="container-fluid" style="width: 100%; padding: 0">
                    <div class="row">
                      <div
                        class="col-6"
                        style="
                          padding-left: 5px;
                          padding-right: 5px;
                          width: 100%;
                        "
                      >
                        <button
                          class="btn btn-primary btn-sm w-100"
                          v-on:click="lineup(supermarket.id)"
                          type="submit"
                        >
                          Line up
                        </button>
                      </div>
                      <div
                        class="col-6"
                        style="
                          padding-left: 5px;
                          padding-right: 5px;
                          width: 100%;
                        "
                      >
                        <button
                          class="btn btn-primary btn-sm w-100"
                          type="submit"
                          @click="bookSupermarket(supermarket.id)"
                        >
                          Book
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </l-popup>
            </l-marker>

            <l-control-zoom position="bottomleft"></l-control-zoom>
          </l-map>
        </client-only>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import VueGeolocation from "vue-browser-geolocation";
export default {
  components: {
    VueGeolocation,
  },

  data: function () {
    return {
      map_lat: 0,
      map_lng: 0,
      map_options: {
        zoomControl: false,
      },
      icon: {},
      customText: "Supermarket",
      staticAnchor: [16, 37],
      supermarkets_list: [],

      filterName: [],
      filterWaitingTime: null,

      filterIsActive: false,

      slider_value: 0,
      supermarkets_names: [],

      popup_message: "",
      display_popup: false,
    };
  },

  methods: {
    ...mapActions({
      getToken: "auth/getToken",
      getUsername: "auth/getUsername",
      store_logout: "auth/logout",
      setSupermarketList: "supermarket/setSupermarketList",
      setSelectedSupermarket: "supermarket/setSelectedSupermarket",
    }),

    /* Get user's location */
    getLocation() {
      VueGeolocation.getLocation().then((coordinates) => {
        this.map_lat = coordinates.lat;
        this.map_lng = coordinates.lng;
        console.log(coordinates);
      });
    },

    /**
     * Deletes token from localStorage and navigates to /login
     */
    async logout() {
      await this.store_logout();
      this.$router.push("/login");
    },

    /**
     * Show popup overlay with the message specified as parameter.
     * @param msg The message to show in the popup.
     */
    showPopup(msg) {
      this.popup_message = msg;
      this.display_popup = true;
    },

    /**
     * Hides the popup and cleans the display message.
     */
    hidePopup() {
      this.popup_message = "";
      this.display_popup = false;
    },

    /**
     * Sets the clicked supermarket (using the parameter s_id) in the store to be persistent between views.
     * Then navigates to /booking
     * @param s_id supermarket id
     */
    async bookSupermarket(s_id) {
      console.log(s_id);
      await this.setSelectedSupermarket(s_id);
      await console.log(this.selected_supermarket);
      this.$router.push("/booking");
    },

    /**
     * Bring the whole list of supermarkets from the database through an endpoint.
     * The supermarkets are loaded when the view is rendered, if there is an error it returns to /login and logs out the user,
     * this is to prevent that non-logged in users enter the app.
     */
    async loadSupermarkets() {
      let token;
      token = await this.getToken();
      fetch("http://127.0.0.1:5000/supermarkets_list", {
        method: "GET",
        headers: {
          Authorization: "JWT " + token,
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          console.log(response);
          if (response.status == 200) {
            response.json().then((data) => {
              console.log("Success:", data);
              this.supermarkets_list = data.supermarkets;
            });
          } else {
            this.logout();
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          this.logout();
        });
    },

    /**
     * Euclidean distance between two points.
     * At short distances we can consider the space to be a plane and use simple euclidean distance.
     */
    getDistance(lat1, lon1, lat2, lon2) {
      let distance = Math.sqrt(
        Math.pow(parseFloat(lat1) - parseFloat(lat2), 2) +
          Math.pow(parseFloat(lon1) - parseFloat(lon2), 2)
      );
      return distance;
    },

    /**
     * Filters the list by taking the value and the checked supermarkets and filtering by them
     */
    async applyFilter() {
      this.filterWaitingTime = this.slider_value;
      this.filterName = [];
      for (let i in this.supermarkets_names) {
        if (this.supermarkets_names[i].active) {
          this.filterName.push(this.supermarkets_names[i].name);
        }
      }
    },

    /**
     * Updates the supermarkets names that are selected to be filtered.
     * This list is shown in the filters.
     */
    updateFilterNames(super_list) {
      if (this.supermarkets_names.length == 0) {
        let sp_list = [];
        for (let i in super_list) {
          let supermarket = super_list[i];
          if (
            sp_list.filter((sp) => sp["name"] === supermarket.name).length == 0
          ) {
            let obj = {
              name: supermarket.name,
              active: false,
            };
            sp_list.push(obj);
          }
        }
        this.supermarkets_names = sp_list;
      }
    },

    /**
     * Filter the supermarkets list that is in data by distance and the selected filters.
     * Calls the updateFilterNames() to update the filters.
     * Returns a new list.
     */
    filterList() {
      let super_list = [];
      for (let i in this.supermarkets_list) {
        let supermarket = this.supermarkets_list[i];
        if (
          this.getDistance(
            this.map_lat,
            this.map_lng,
            supermarket.lat,
            supermarket.lon
          ) < 0.02
        ) {
          super_list.push(supermarket);
        }
      }

      this.updateFilterNames(super_list);
      super_list = super_list.filter((element) => {
        if (this.filterWaitingTime != null) {
          if (element.waiting_time > this.filterWaitingTime) {
            return false;
          }
        }

        // Updates the list with the selected supermarket filters
        if (this.filterName.length > 0) {
          let name_exists = false;
          for (let i in this.filterName) {
            let name = this.filterName[i];
            if (element.name == name) {
              name_exists = true;
            }
          }
          if (!name_exists) {
            return false;
          }
        }
        return true;
      });
      return super_list;
    },

    /**
     * Clears filters and shows all nearby supermarkets.
     */
    clearFilter() {
      for (let i in this.supermarkets_names) {
        let supermarket = this.supermarkets_names[i];
        supermarket.active = false;
      }
      this.applyFilter();
    },

    /**
     * Receives a user and a supermarkets and performs the line up by sending a request to the backend (/lineup).
     * If the request was successful then it automatically shows the qrcode view with the user's token to enter the
     * supermarket in a specific time shown, else shows a popup with the error.
     */
    async lineup(sm_id) {
      let token = await this.getToken();
      const data = { supermarket_id: sm_id, username: this.username };
      fetch("http://127.0.0.1:5000/lineup", {
        method: "POST",
        headers: {
          Authorization: "JWT " + token,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          console.log(response);
          if (response.status == 201) {
            this.lineup_success = true;
            response.json().then((data) => {
              if (this.lineup_success) {
                this.$router.push("/qrcode");
              }
            });
          } else {
            this.showPopup("Could not request lineup!");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
  },

  computed: {
    ...mapGetters({
      auth: "auth/getAuthState",
      username1: "auth/getUsername",
      selected_supermarket: "supermarket/getSelectedSupermarket",
      stored_supermarkets_list: "supermarket/getSupermarketList",
    }),

    /**
     * Dynamic function to update the list of nearby supermarkets
     */
    new_supermarkets_list: function () {
      let super_list = this.filterList();
      this.setSupermarketList(super_list);
      return super_list;
    },
  },

  async mounted() {
    //gets user location
    this.getLocation();

    this.icon = this.$L.icon({
      iconUrl:
        "https://upload.wikimedia.org/wikipedia/commons/8/88/Map_marker.svg",
      iconSize: [30, 42],
      iconAnchor: [15, 42], // half of width + height
    });
    
    // load all supermarkets from the database
    this.loadSupermarkets();
    this.username = await this.getUsername();
  },
};
</script>

<style>
.map-container {
  margin: 0;
  width: 100% !important;
  height: 100vh;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.supermarket-card {
  width: 90px;
  padding: 5px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.3s;
  border-radius: 5px; /* 5px rounded corners */
  justify-content: center;
  align-items: center;
  text-align: center;
}

.card:hover {
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
}

/* Add rounded corners to the top left and the top right corner of the image */
img {
  border-radius: 10px 10px 0 0;
}

.waiting-time {
  padding: 10px;
  text-align: center;
  display: block;
}

.title {
  font-family: Roboto;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}

.marker-pin {
  width: 30px;
  height: 30px;
  border-radius: 50% 50% 50% 0;
  background: #c30b82;
  position: absolute;
  transform: rotate(-45deg);
  left: 50%;
  top: 50%;
  margin: -15px 0 0 -15px;
}
/* to draw white circle */
.marker-pin::after {
  content: "";
  width: 24px;
  height: 24px;
  margin: 3px 0 0 3px;
  background: #fff;
  position: absolute;
  border-radius: 50%;
}

/* to align icon */
.custom-div-icon i {
  position: absolute;
  width: 22px;
  font-size: 22px;
  left: 0;
  right: 0;
  margin: 10px auto;
  text-align: center;
}
.search {
  width: 100%;
  position: relative;
  display: flex;
}

.searchTerm {
  width: 100%;
  border: 3px solid #adc1c4;
  border-right: none;
  padding: 5px;
  height: 36px;
  border-radius: 10px;
  outline: none;
  color: #9dbfaf;
}

.searchTerm:focus {
  color: #adc1c4;
}

.searchButton {
  width: 40px;
  height: 36px;
  border: 1px solid #adc1c4;
  background: #adc1c4;
  text-align: center;
  color: #fff;
  border-radius: 10px;
  cursor: pointer;
  font-size: 20px;
}

/*Resize the wrap to see the search bar change!*/
.wrap {
  width: 100%;
  position: absolute;
  top: 50px;
  left: 50%;
  padding: 0px 10px;
  transform: translate(-50%, -50%);
  z-index: 100;
}

.button-bar {
  position: absolute;
  width: 90px;
  height: 180px;
  z-index: 9999;
  right: 0;
  bottom: 0;
}

.round-button {
  width: 50px;
  height: 50px;
  font-size: 20px;
  z-index: 88888;
  background-color: rgb(6, 106, 255);
  margin: 0 auto 10px auto;
  border-radius: 50%;
  text-align: center;
  color: white;
  cursor: pointer;
  box-shadow: 3px 4px 5px #888888;
}

.round-button-icon {
  margin-top: 14px;
  font-size: 22px;
  color: white;
}

/* for filter according to waiting time: red, green and yellow*/
.red-marker {
  background-color: #c43939;
}

.green-marker {
  background-color: #27bd2e;
}

.yellow-marker {
  background-color: #c2bf1a;
}

.filter-popup {
  width: 190px;
  height: 250px;
  border-radius: 5px;
  position: absolute;
  z-index: 99999;
  background: white;
  border: 0px solid #333333;
  top: -250px;
  left: -190px;
  color: #333333;
  overflow: scroll;
  box-shadow: 3px 4px 5px #888888;
}

.slidecontainer {
  width: 100%; /* Width of the outside container */
  text-align: center;
}

.check {
  padding: 0px 10px;
}

button {
  background-color: #4a0d70;
  color: white;
  border-radius: 4px;
  padding: 8px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 50%;
}

button:hover {
  opacity: 0.8;
}

.popup-title {
  font-weight: bold;
  text-align: center;
}

.overlay {
  width: 100%;
  height: 100vh;
  position: absolute;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 999;
}

.popup {
  margin: auto auto;
  background-color: white;
  border-radius: 5px;
  z-index: 1000;
  top: 25%;
  width: 200px;
  padding: 20px;
  text-align: center;
  opacity: 1;
  position: relative;
}

.round-logout-button {
  cursor: pointer;
  width: 50px;
  height: 50px;
  font-size: 20px;
  z-index: 88888;
  background-color: rgb(6, 106, 255);
  margin: 0 auto 10px auto;
  border-radius: 50%;
  text-align: center;
  color: white;
  cursor: pointer;
  position: absolute;
  right: 10px;
  top: 10px;
}

.round-logout-button-icon {
  margin-top: 14px;
  font-size: 22px;
  color: white;
}
</style>
