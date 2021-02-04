<template>
    <div>
        <div class="container">
            <img src="../assets/img/logo_clup_black_large.png" >
            <h3 style="text-align:left; padding-top:20px; padding-bottom:20px;">Buy as soon as possible</h3>
            <div 
                v-for="supermarket in stored_supermarkets_list"
                :key="supermarket.id"
            >
                <div class="card border-secondary mb-3" :class="{'red-marker': supermarket.waiting_time >= 300, 'yellow-marker': supermarket.waiting_time < 300 && supermarket.waiting_time >= 60, 'green-marker': supermarket.waiting_time < 60}">
                    <div class="card-body">
                        <h5 class="card-title">{{supermarket.name}}</h5>
                        <p class="card-text">{{supermarket.waiting_time}} minutes waiting time</p>
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
import {mapActions, mapGetters} from 'vuex';
export default {
    data: function () {
      return {
      }
    },
    methods: {
        ...mapActions({
            getToken: "auth/getToken", 
            getUsername: "auth/getUsername",
            setSupermarketList: "supermarket/setSupermarketList",
            setSelectedSupermarket: "supermarket/setSelectedSupermarket",
        }),
        /* login function to send data and get a response from the server */ 
        async LineUpSupermarket(s_id){
            console.log(s_id);
            await this.setSelectedSupermarket(s_id);
            await console.log(this.selected_supermarket);
            this.lineup(selected_supermarket);
        },

        async lineup(sm_id){
            let token = await this.getToken();
            let username = await this.username;
            console.log(username);
            const data = { supermarket_id: sm_id, username: username };
            fetch('http://127.0.0.1:5000/lineup', {
            method: 'POST',
            headers: {
                'Authorization': 'JWT ' + token,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
            })
            .then(response => {
            console.log(response);
            })
            .catch((error) => {
            console.error('Error:', error);
            });
        },

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

    /* for filter according to waiting time: red, green and yellow*/
    .red-marker{
    background-color: #c43939;
    }

    .green-marker{
    background-color: #27bd2e;
    }

    .yellow-marker{
    background-color: #c2bf1a;
    }
</style>