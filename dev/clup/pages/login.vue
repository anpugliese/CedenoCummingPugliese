<template>
    <div>
        <!-- Login form -->
        <div class="container">
            <img src="../assets/img/logo_clup_black_large.png" >
            <h3 style="text-align:left; padding-top:20px; padding-bottom:20px;">Login</h3>
        
            <label for="username"><h6 style="color: #4a0d70;">Username</h6></label>
            <input v-model="username" type="text" placeholder="example@email.com" name="username" required>

            <label for="password"><h6 style="color: #4a0d70;">Password</h6></label>
            <input v-model="password" type="password" placeholder="password" name="password" required>
                
            <button @click="login()" type="submit"><b>Login</b></button>
            
        </div>

        <div class="container">
            <p>Or create an account <span class="highlight"><NuxtLink to="/register" style="color: #4a0d70; font-weight: bold;">Sign up</NuxtLink></span></p>
        </div>
        
    </div>
</template>

<script>
import {mapActions, mapGetters} from 'vuex';

export default {
    data: function () {
      return {
        username: '',
        password: '',
        login_success: false,
      }
    },
    methods: {

        ...mapActions({saveToken: "auth/login"}),

        /* login function to send data and get a response from the server */ 
        login(){
            const data = { username: this.username, password: this.password };
            let savedUsername = this.username;
            console.log(savedUsername);

            fetch('http://127.0.0.1:5000/auth', {
            method: 'POST', // or 'PUT'
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
            })
            .then(response => {
                
                console.log(response);
                if(response.status == 200){
                    this.login_success = true;
                    response.json().then(data => {
                        console.log('Success:', data);
                        if(this.login_success){
                            console.log(savedUsername);
                            this.saveToken({token: data.access_token, username: savedUsername});
                            this.$router.push("/");
                        }
                    })
                } 
            })
            .catch((error) => {
            console.error('Error:', error);
            });
        }

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