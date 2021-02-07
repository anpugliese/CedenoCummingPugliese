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

    <!-- Booking form -->
    <div class="container">
      <img src="../assets/img/logo_clup_black_large.png" />
      <h3 style="text-align: left; padding-top: 20px; padding-bottom: 20px">
        Booking {{ selected_supermarket_name }}
      </h3>
      <h5 style="color: #4a0d70">Hello {{ username }}!</h5>
      <h5 style="color: #4a0d70">Please select your date and time:</h5>

      <br />
      <div class="my-3 p-1">
        <label><h6 style="color: #4a0d70">Booking date:</h6></label>
        <input
          type="date"
          v-model="bookingDate"
          :min="today"
          name="booking-datetime"
        />
      </div>
      <div class="my-3 p-1">
        <label><h6 style="color: #4a0d70">Booking time:</h6></label>
        <input type="time" v-model="bookingTime" name="booking-datetime" />
      </div>

      <button @click="booking()" type="submit"><b>Book</b></button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
  data: function () {
    return {
      bookingDate: "",
      bookingTime: "",
      username: "",
      supermarket_id: "",
      shop_time: "",
      selected_supermarket_name: "",
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
      this.popup_message = msg;
      this.display_popup = true;
    },
    hidePopup() {
      this.popup_message = "";
      this.display_popup = false;
    },

    async booking() {
      let token = await this.getToken();
      let date = this.bookingDate;
      let time = this.bookingTime;
      let datetime = date + " " + time;
      const data = {
        username: this.username,
        supermarket_id: this.selected_supermarket,
        shop_time: datetime,
      };
      fetch("http://127.0.0.1:5000/booking", {
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
            this.booking_success = true;
            response.json().then((data) => {
              console.log("Success:", data);
              if (this.booking_success) {
                this.$router.push("/qrcode");
              }
            });
          } else if (response.status == 403) {
            this.showPopup("Please select another date or time!");
          } else if (response.status == 401)
            this.showPopup("You already have a booking!");
          else {
            this.showPopup("Please select date and time!");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },

    async seletedSupermarketName() {
      for (let i in await this.stored_supermarkets_list) {
        let supermarket = this.stored_supermarkets_list[i];
        if (supermarket.id == this.selected_supermarket) {
          this.selected_supermarket_name = supermarket.name;
        }
      }
    },
  },

  computed: {
    ...mapGetters({
      auth: "auth/getAuthState",
      username1: "auth/getUsername",
      selected_supermarket: "supermarket/getSelectedSupermarket",
      stored_supermarkets_list: "supermarket/getSupermarketList",
    }),

    today() {
      let now = new Date();
      return now.toISOString().slice(0, 10);
    },
  },

  async mounted() {
    this.username = await this.getUsername();
    this.seletedSupermarketName();
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
button {
  background-color: #4a0d70;
  color: white;
  border-radius: 4px;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
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