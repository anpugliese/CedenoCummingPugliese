<template>

    <div>
        
        <!-- Login form -->
        <div class="container">
            <img src="../assets/img/logo_clup_black_large.png" >
            <h3 style="text-align:lefdt; padding-top:20px; padding-bottom:20px;">Booking {{selected_supermarket_name}}</h3>
            <h5 style="color: #4a0d70;">Hello {{username}}!</h5>
            <h5 style="color: #4a0d70;">Please select your date and time:</h5>
            <!-- <h5>the selected supermarket is {{selected_supermarket}}</h5> -->
            
            <!-- <label for="datetime"><h6 style="color: #4a0d70;">Date and Time</h6></label> -->
            <!-- <label for="username"><h6 style="color: #4a0d70;">Username</h6></label>
            <input v-model="username" type="text" placeholder="enter user id..."> -->
<!--             
            <label><h6 style="color: #4a0d70;">Date and Time:</h6></label> -->
            <br>
            <label><h6 style="color: #4a0d70;">Year:</h6></label>
            <select v-model="year" type="text">
                <option>2021</option>
                <option>2022</option>
            </select>
            <label><h6 style="color: #4a0d70;">Month:</h6></label>
            <select v-model='month' type = "text">
                <option>01</option>
                <option>02</option>
                <option>03</option>
                <option>04</option>
                <option>05</option>
                <option>06</option>
                <option>07</option>
                <option>08</option>
                <option>09</option>
                <option>10</option>
                <option>11</option>
                <option>12</option>
            </select>
            <label><h6 style="color: #4a0d70;">Day:</h6></label>
            <select v-model="day" type = "selected">
                <option>01</option>
                <option>02</option>
                <option>03</option>
                <option>04</option>
                <option>05</option>
                <option>06</option>
                <option>07</option>
                <option>08</option>
                <option>09</option>
                <option>10</option>
                <option>11</option>
                <option>12</option>
                <option>13</option>
                <option>14</option>
                <option>15</option>
                <option>16</option>
                <option>17</option>
                <option>18</option>
                <option>19</option>
                <option>20</option>
                <option>21</option>
                <option>22</option>
                <option>23</option>
                <option>24</option>
                <option>25</option>
                <option>26</option>
                <option>27</option>
                <option>28</option>
                <option>29</option>
                <option>30</option>
                <option>31</option>
            </select>
            <label><h6 style="color: #4a0d70;">Hour:</h6></label>
            <select v-model="hour" type = "selected">
                <option>01</option>
                <option>02</option>
                <option>03</option>
                <option>04</option>
                <option>05</option>
                <option>06</option>
                <option>07</option>
                <option>08</option>
                <option>09</option>
                <option>10</option>
                <option>11</option>
                <option>12</option>
                <option>13</option>
                <option>14</option>
                <option>15</option>
                <option>16</option>
                <option>17</option>
                <option>18</option>
                <option>19</option>
                <option>20</option>
                <option>21</option>
                <option>22</option>
                <option>23</option>
                <option>24</option>
            </select>
            <label><h6 style="color: #4a0d70;">Minute:</h6></label>
            <select v-model="minute" type = "selected">
                <option>00</option>
                <option>30</option>                
                <!-- <option v-for="index in 60" :key="index">{{index}}</option> -->
            </select>
            <br>
            <!-- <input v-model="shop_time" type="text" placeholder="2021-03-01 16:00:00"> -->
            <!-- <label for="supermarket_id"><h6 style="color: #4a0d70;">Supermarket ID</h6></label>
            <input v-model="supermarket_id" type="text" placeholder="123"> -->
            <button @click="booking()" type="submit"><b>Book</b></button>
            
        </div>
        
    </div>
</template>

<script>
    // import Datetime from 'vue-datetime';
    import {mapActions, mapGetters} from 'vuex';
    export default{
            
        data: function () {
            return {
                username: '',
                supermarket_id: '',
                shop_time: '',
                year: '',
                month:'',
                day:'',
                hour:'',
                minute:'',
                selected_supermarket_name: '',

            }
        },
        methods: {
            ...mapActions({
                getToken: "auth/getToken", 
                getUsername: "auth/getUsername",
                setSupermarketList: "supermarket/setSupermarketList",
                setSelectedSupermarket: "supermarket/setSelectedSupermarket",
            }),
            
            /*  showFlashMessage(element){
                var event = new CustomEvent('showFlashMessage');
                element.dispatchEvent(event);
            }, */
            /* register function to send data and get a response from the server */ 
            async booking(){     
                let token = await this.getToken();           
                // datestr = datestr.concat(String(year), "-", String(month))
                const data = { username: this.username,  supermarket_id: this.selected_supermarket, shop_time: this.year+'-'+this.month+'-'+this.day+' '+this.hour+':'+this.minute }
                fetch('http://127.0.0.1:5000/booking', {
                method: 'POST', 
                headers: {
                    'Authorization': 'JWT ' + token,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
                })
                .then(response => {
                    
                    console.log(response);
                    if(response.status == 201){
                        this.booking_success = true;
/*                         var flashMessages = document.getElementsByClassName('js-flash-message');
                        //show first flash message avilable in your page
                        showFlashMessage(flashMessages[0]); */
                        response.json().then(data => {
                            console.log('Success:', data);
                            if(this.booking_success){
                                alert('You successfully booked!')
                                this.$router.push("/");
                            }
                        })
                    
                    }else if(response.status == 400) {
                        alert('Please select another date or time!')
                    }else if(response.status == 401)
                        alert('You already have a booking!')
                })
                .catch((error) => {
                console.error('Error:', error);
                });
            },

            async seletedSupermarketName(){
                for(let i in await this.stored_supermarkets_list){
                    let supermarket = this.stored_supermarkets_list[i];
                    if(supermarket.id == this.selected_supermarket){
                        this.selected_supermarket_name = supermarket.name;
                    }
                }
            }
        },

        computed: {
            ...mapGetters({ 
                auth: "auth/getAuthState" , 
                username1: "auth/getUsername",
                selected_supermarket: "supermarket/getSelectedSupermarket",
                stored_supermarkets_list: "supermarket/getSupermarketList"
            }),
        },

        async mounted(){
            this.username = await this.getUsername();
            this.seletedSupermarketName();
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