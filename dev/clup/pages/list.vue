<template>
    <div>
        <h4>Buy as soon as possible</h4>
        <h5>{{token}}</h5>
        
    </div>
</template>

<script>
export default {
    data: function () {
      return {
        selected_supermarket: '',
        token: '',
      }
    },
    methods: {
        /* login function to send data and get a response from the server */ 
        lineUp(){
            const data = { username: this.username, supermarket: this.supermarket };

            fetch('http://127.0.0.1:5000/xxx', {
            method: 'POST', // or 'PUT'
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
            })
            .then(response => {
                
                console.log(response);
                if(response.status == 200){

                    response.json().then(data => {
                        console.log('Success:', data);
                        
                    })
                } 
            })
            .catch((error) => {
            console.error('Error:', error);
            });
        }

    },

    mounted(){
        this.token = this.$token;
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