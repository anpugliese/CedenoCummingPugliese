<template>

    <div>
        
        <!-- Login form -->
        <div class="container">
            <img src="../assets/img/logo_clup_black_large.png" >
            <h3 style="text-align:lefdt; padding-top:20px; padding-bottom:20px;">Your QRCode:</h3>
            <!-- <h5 style="color: #4a0d70;">Hello {{username}} :</h5> -->
            <div v-if="!loading">
                <vue-qrcode :value="qr_code" :width="300"/>
            </div>
        </div>
        
    </div>
</template>


 <script>
import {mapActions, mapGetters} from 'vuex';
import VueQrcode from 'vue-qrcode';
 
export default{

  components: {
    VueQrcode,
  },
    data: function () {
        return {
            username: '',
            supermarket_id: '',
            value:"token",
            width: '300',
            qr_code: 'loquesea',
            loading: true,
            register_success: false
        }
    },
    methods: {
    ...mapActions({
        getToken: "auth/getToken", 
        getUsername: "auth/getUsername",
    }),

      

      async qrCode(){
        let token = await this.getToken();  
        // const data = { username: this.username }
        const data = { username: this.username }
        fetch('http://127.0.0.1:5000/qrcode', {
          method: 'POST',
          headers: {
              'Authorization': 'JWT ' + token,
              'Content-Type': 'application/json',
          },
            body: JSON.stringify(data),
              })
            .then(response => {                    
                    console.log(response);
                    if(response.status == 200){
                        response.json().then(data => {
                            console.log('Success:', data);
                            this.qr_code = data.qr_code;
                        })
                    
                    }else if (response.status != 200) {
                        this.qr_code = '';
                        this.$router.push("/");
                    }
                });
           
      },


}, 



        computed: {
            ...mapGetters({ 
                auth: "auth/getAuthState" , 
                username1: "auth/getUsername",
            }),
        },

        async mounted(){
            this.value = "hello";
            this.username = await this.getUsername();
            this.loading = true;
            await this.qrCode();
            this.loading = false;
        }

}
</script>





<style scoped>
    
    input[type=text], input[type=password] {
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
    span.highlight{
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
</style>