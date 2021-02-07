<template>
  <div>
    <!-- Popup -->
    <div class="round-back-button">
      <NuxtLink to="/">
        <fa-icon
          :icon="['fas', 'chevron-left']"
          class="round-back-button-icon"
        />
      </NuxtLink>
    </div>
    <!-- QR code view -->
    <div class="container">    
      <img src="../assets/img/logo_clup_black_large.png" />
      <div v-if="!loading">
        <div v-if="no_qr" class="text-center">
          <h2>No QR code available. Please request a ticket.</h2>
        </div>
        <div v-else class="text-center">
          <h3 style="text-align: center; padding-top: 20px; padding-bottom: 0px">
            Your QRCode to enter {{supermarket_name}}:
          </h3> 
          <vue-qrcode :value="qr_code" :width="300" />
            <!-- Waiting time view, activated when waiting time is larger than 0  -->
          <div v-if="!time_exp" class="text-center">
            <h3
              style="text-align: center; padding-top: 0px; padding-bottom: 0px"
            >
              Your waiting time: 
              {{ remain_time_hours }}hours
              {{ remain_time_min }}min
            </h3>
          </div>
          <div v-if="time_exp" class="text-center">
            <!-- 5 minutes coundown view, activated when waiting time is smaller than 0  -->
            <h3
              style="text-align: center; color: red; padding-top: 0px; padding-bottom: 0px"
            >
              Your QRCode is about to expire:
            </h3>
            <h3
              style="text-align: center; color: red; padding-top: 0px; padding-bottom: 0px"
            >
              {{ enter_time }}sec
            </h3>
          </div>
        </div>
      </div>
      <div v-if="loading" class="text-center w-100">
        <div class="lds-dual-ring"></div>
      </div>
    </div>

    <!-- Go back to map -->
    <div class="text-center mt-5">
      <NuxtLink to="/" class="back-button" style="color:white"> 
        <span>Go back to map</span>
      </NuxtLink>
    </div>
    <div v-if="!no_qr" class="text-center mt-5">
    <!-- Cancel Booking or Line up -->
      <button @click="cancel()" class="back-button" style="color:white; width: 50%;"><span>Cancel request</span></button>
    </div>
  </div>
</template>


 <script>
import { mapActions, mapGetters } from "vuex";
import VueQrcode from "vue-qrcode";

export default {
  components: {
    VueQrcode,
  },
  data: function () {
    return {
      username: "",
      supermarket_id: "",
      value: "token",
      width: "300",
      qr_code: "loquesea",
      remain_time_min: "",
      remain_time_hours: "",
      remain_time: "",
      supermarket_name: "",
      enter_time: "",
      countDown: 300,
      loading: true,
      register_success: false,
      refresh: {},
      no_qr: true,
      time_exp: false,
    };
  },
  methods: {
    ...mapActions({
      getToken: "auth/getToken",
      getUsername: "auth/getUsername",
    }),

    /* Get QR code of username */
    async qrCode() {
      let token = await this.getToken();
      const data = { username: this.username };
      fetch("http://127.0.0.1:5000/qrcode", {
        method: "POST",
        headers: {
          Authorization: "JWT " + token,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }).then((response) => {
        console.log(response);
        if (response.status == 200) {
          response.json().then((data) => {
            console.log("Success:", data);
            this.qr_code = data.qr_code;
            this.supermarket_name = data.supermarket_name;
            this.no_qr = false;
          });
        } else if (response.status != 200) {
          this.qr_code = "loquesea";
          this.no_qr = true;
        }
      });
    },

    /* Update remaining time to enter supermarket */
    async remainingTime() {
      let token = await this.getToken();
      await this.qrCode();
      const data = { username: this.username };
      fetch("http://127.0.0.1:5000/remainingTime", {
        method: "POST",
        headers: {
          Authorization: "JWT " + token,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }).then((response) => {
        console.log(response);
        if (response.status == 200) {
          response.json().then((data) => {
            console.log("Success:", data);
            this.remain_time_min = data.remain_time_min;
            this.remain_time_hours = data.remain_time_hours;
            this.remain_time = data.wait_time;
            this.enter_time = data.enter_time;
          });
          if (this.remain_time==0){
            this.time_exp = true;
          }else{
            this.time_exp = false;
          }
        }
      });
    },
      // count down timer to display when QRCode is from 5 min to expire
      async countDownTimer() {
        if(this.enter_time==0){
                if(this.countDown > 0) {
                    this.$router.push("/")
                }
                else{}
        }else{}
      },

    /* Cancel Booking or Line up */
    async cancel(){
      let token = await this.getToken();
      await this.qrCode();
      const data = { username: this.username };
      fetch("http://127.0.0.1:5000/cancelFun", {
        method: "POST",
        headers: {
          Authorization: "JWT " + token,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }).then((response) => {
        console.log(response);
        if (response.status == 200) {
          this.showPopup("Please select another date or time!");
        }
      });
      
    }
  },

  computed: {
    ...mapGetters({
      auth: "auth/getAuthState",
      username1: "auth/getUsername",
    }),
  },

  async mounted() {
    this.loading = true;
    this.value = "hello";
    this.username = await this.getUsername();
    await this.qrCode();
    this.loading = false;
    await this.remainingTime();
    this.refresh = setInterval(() => {
      this.remainingTime();
    }, 500);
    this.countTimer = setInterval(() => {
        this.countDownTimer();
    }, 1000);
  },

  destroyed() {
    clearInterval(this.refresh);
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
  width: 50%;
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

.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}
.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid rgb(163, 163, 163);
  border-color: rgb(163, 163, 163) transparent rgb(163, 163, 163) transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.back-button{
  background-color: #4a0d70;
  color: white;
  border-radius: 4px;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
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