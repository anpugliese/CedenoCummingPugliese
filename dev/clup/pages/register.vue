<template>
    <div>
        <div class="container">
            <!-- Register form (more fields may be added) -->
            <img src="../assets/img/logo_clup_black_large.png" >
            <h3 style="text-align:left; padding-top:20px; padding-bottom:20px;">Sign up</h3>
        
            <label for="username"><h6 style="color: #4a0d70;">Username</h6></label>
            <input v-model="username" type="text" placeholder="example@email.com" name="username" required>

            <label for="password"><h6 style="color: #4a0d70;">Password</h6></label>
            <input v-model="password" type="password" placeholder="password" name="password" required>
            <label style="font-size: 12px; padding: 10px 0px;">
            <input type="checkbox" checked="checked" name="remember"> I agree to the <span class="highlight"><b>Terms of Service</b></span> and <span class="highlight"><b>Privacy Policy</b></span>
            </label>
                
            <button @click="register()" type="submit"><b>Continue</b></button>
            
        </div>

        <div style="padding: 0px 30px;">
            <p>Have an account? <span class="highlight"><NuxtLink to="/login" style="color: #4a0d70; font-weight: bold;">Log in</NuxtLink></span></p>
        </div>
        
    </div>
</template>

<script>
export default {
    data: function () {
      return {
        username: '',
        password: '',
        register_success: false,
      }
    },
    methods: {
        /* register function to send data and get a response from the server */ 
        register(){
            const data = { username: this.username, password: this.password };

            fetch('http://127.0.0.1:5000/register', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
            })
               .then(response => {
                
                console.log(response);
                if(response.status == 201){
                    this.register_success = true;
                    response.json().then(data => {
                        console.log('Success:', data);
                        if(this.register_success){
                            this.$router.push("/login");
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