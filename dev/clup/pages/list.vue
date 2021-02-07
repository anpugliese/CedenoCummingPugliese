<template>
  <div>
		<div class="overlay" @click="hidePopup()" v-if="display_popup">
      <div class="popup">
        <h4>{{ popup_message }}</h4>
      </div>
    </div>
    <div class="round-back-button">
      <NuxtLink to="/">
        <fa-icon
          :icon="['fas', 'chevron-left']"
          class="round-back-button-icon"
        />
      </NuxtLink>
    </div>
    <div class="container">
      <img src="../assets/img/logo_clup_black_large.png" />
      <h3 style="text-align: left; padding-top: 20px; padding-bottom: 20px">
        Buy as soon as possible
      </h3>
      <div
        v-for="supermarket in stored_supermarkets_list"
        :key="supermarket.id"
      >
        <div
          class="card border-secondary mb-3"
          :class="{
            'red-marker': supermarket.waiting_time >= 300,
            'yellow-marker':
              supermarket.waiting_time < 300 && supermarket.waiting_time >= 60,
            'green-marker': supermarket.waiting_time < 60,
          }"
        >
          <div class="card-body">
            <h5 class="card-title">{{ supermarket.name }}</h5>
            <p class="card-text">
              {{ supermarket.waiting_time }} minutes waiting time
            </p>
            <button
              class="btn btn-primary btn-sm w-100"
              type="submit"
              @click="LineUpSupermarket(supermarket.id)"
            >
              Line up
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
  data: function () {
    return {
      ordered_list: [],
      lineup_success: false,
      popup_message: "",
      display_popup: false,
    };
  },
  methods: {
    ...mapActions({
      getToken: "auth/getToken",
      getUsername: "auth/getUsername",
      setSupermarketList: "supermarket/setSupermarketList",
      setSelectedSupermarket: "supermarket/setSelectedSupermarket",
    }),
    showPopup(msg) {
			document.documentElement.scrollTop = 0;
      this.popup_message = msg;
      this.display_popup = true;
    },
    hidePopup() {
      this.popup_message = "";
      this.display_popup = false;
    },
    /* login function to send data and get a response from the server */
    async LineUpSupermarket(s_id) {
      console.log(s_id);
      await this.setSelectedSupermarket(s_id);
      await console.log(this.selected_supermarket);
      this.lineup(this.selected_supermarket);
    },

    async lineup(sm_id) {
      let token = await this.getToken();
      let username = await this.username;
      console.log(username);
      const data = { supermarket_id: sm_id, username: username };
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
					}
					else {
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
  },

  async mounted() {
    this.username = await this.getUsername();
    let supermarkets = JSON.parse(
      JSON.stringify(await this.stored_supermarkets_list)
    );
    let ordered_supermarkets = supermarkets.sort((a, b) => {
      return a.waiting_time <= b.waiting_time;
    });
    this.setSupermarketList(ordered_supermarkets);
    console.log(ordered_supermarkets);
  },
};
</script>

<style scoped>
input[type="text"],
input[type="password"] {
  width: 100%;
  margin: 8px 0;
  display: inline-block;
  border-top: none;
  border-left: none;
  border-right: none;
  border-bottom: 1px solid #ccc;
}

button:hover {
  opacity: 0.8;
}

img {
  display: block;
  margin-left: auto;
  margin-right: auto;
  height: 70%;
}

span.highlight {
  color: #4a0d70;
}

.container {
  padding: 30px;
}

span.psw {
  float: right;
  padding-top: 16px;
}

/* Change styles for span and cancel button on extra small screens */
@media screen and (max-width: 300px) {
  span.psw {
    display: block;
    float: none;
  }
  .cancelbtn {
    width: 100%;
  }
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

.round-back-button {
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
  left: 10px;
  top: 10px;
}

.round-back-button-icon {
  margin-top: 14px;
  font-size: 22px;
  color: white;
}
</style>