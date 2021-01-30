<template>
<div>
  <!-- Button bar in the three bottom left  -->
  <div class="button-bar">
    <div class="round-button">
      <fa-icon :icon="['fas', 'filter']" class="round-button-icon"/>
    </div>

    <div class="round-button">
      <fa-icon :icon="['fas', 'running']" class="round-button-icon"/>
    </div>

    <div class="round-button">
      <fa-icon :icon="['fas', 'qrcode']" class="round-button-icon"/>
    </div>
  </div>

  <!-- Search bar (non functional yet) -->
  <div class="wrap">
   <div class="search">
        <input type="text" class="searchTerm" placeholder="Search for a supermarket">
        <button type="submit" class="searchButton">
          <fa-icon :icon="['fas', 'search']" />
          
        </button>
    </div>
  </div>
  <!-- Render leaflet map -->
  <div class="map-container">
    <div id="map-wrap" style="height: 100%; width: 100%">
    <client-only>
      <l-map :zoom=13 :center="[map_lat, map_lng]" :options="map_options">
        <l-tile-layer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"></l-tile-layer>

        <!-- Iterate to render nearby supermarkets markers -->
        <l-marker 
          v-for="supermarket in new_supermarkets_list"
          :key="supermarket.id"
          :lat-lng="[supermarket.lat, supermarket.lon]" 
          :icon="icon" 
        >
          <l-icon
            :icon-anchor="staticAnchor"
            class-name="someExtraClass"
          >
          <!-- Filter according to waiting time (now just max capacity, waiting time has to be added) -->
            <div class="supermarket-card" style="margin: 2px;"
              :class="{'red-marker': supermarket.max_capacity < 10, 'green-marker': supermarket.max_capacity < 30 && supermarket.max_capacity >= 10}"
            >
              <div style="background-color: white;">
                <img width="50" src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Carrefour_logo.svg/1000px-Carrefour_logo.svg.png">
              </div>    
              <span class="waiting-time">{{supermarket.name}}</span>          
              <span class="waiting-time">{{supermarket.waiting_time}} MINS</span>
            </div>
          </l-icon>
        </l-marker>

        <l-control-zoom position="bottomleft"  ></l-control-zoom>
      </l-map>
    </client-only>
    </div>
  </div>
</div>
</template>

<script>
  
  import VueGeolocation from 'vue-browser-geolocation';
  export default{
    components: {
      VueGeolocation
    },
    
    
    data: function () {
      return {
        map_lat : 0,
        map_lng : 0,
        map_options: {
          zoomControl: false
        },
        icon: {},
        customText: "Supermarket",
        staticAnchor: [16, 37],
        supermarkets_list : [],
      }
    },
    
    methods: {
      /* Get user's location */
      getLocation(){
        VueGeolocation.getLocation()
        .then(coordinates => {
          this.map_lat = coordinates.lat;
          this.map_lng = coordinates.lng;
          console.log(coordinates);
        });
      },

      /* Bring the whole list of supermarkets from the database thru an endpoint */
      loadSupermarkets(){
        fetch('http://127.0.0.1:5000/supermarkets_list', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
        })
        .then(response => {
          console.log(response);
          if(response.status == 200){
            response.json().then(data => {
              console.log('Success:', data);
              this.supermarkets_list = data.supermarkets;
            })
          } 
        })
        .catch((error) => {
        console.error('Error:', error);
        });
      },

      /* Distance between two points */
      getDistance(lat1, lon1, lat2, lon2){
        let distance = Math.sqrt(Math.pow((parseFloat(lat1) - parseFloat(lat2)), 2) + Math.pow((parseFloat(lon1) - parseFloat(lon2)), 2));
        return distance;
      },
      
    },

    computed: {
      /* Dynamic function to update the list of nearby supermarkets */
      new_supermarkets_list: function(){
        let super_list = []; 
        for(let i in this.supermarkets_list){
          let supermarket = this.supermarkets_list[i];
          if(this.getDistance(this.map_lat, this.map_lng, supermarket.lat, supermarket.lon) < 0.02){
            super_list.push(supermarket)
          }
        }
        return super_list
      }
    },

    mounted(){
      this.getLocation();
      this.icon = this.$L.icon({
        iconUrl: "https://upload.wikimedia.org/wikipedia/commons/8/88/Map_marker.svg",
        iconSize: [30, 42],
        iconAnchor: [15, 42] // half of width + height
      })
      this.loadSupermarkets();
    }
  }


</script>

<style>
.map-container {
  margin: 0;
  width: 100%!important;
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
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.3s;
  border-radius: 5px; /* 5px rounded corners */
  justify-content: center;
  align-items: center;
  text-align: center;
}

.card:hover {
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}

/* Add rounded corners to the top left and the top right corner of the image */
img {
  border-radius: 10px 10px 0 0;
}

.waiting-time{
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
    content: '';
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
  color: #9DBFAF;
}

.searchTerm:focus{
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
.wrap{
  width: 100%;
  position: absolute;
  top: 50px;
  left: 50%;
  padding: 0px 10px;
  transform: translate(-50%, -50%);
  z-index: 100000;
}

.button-bar{
  position: absolute;
  width: 90px;
  height: 180px;
  z-index: 9999;
  right: 0;
  bottom: 0;
}

.round-button{
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

.round-button-icon{
  margin-top: 14px;
  font-size: 22px;
}

/* for filter according to waiting time: red, green and yellow*/
.red-marker{
  background-color: #c43939;
}

.green-marker{
  background-color: #2bb660;
}

.yellow-marker{
  background-color: #c2bf1a;
}

</style>
