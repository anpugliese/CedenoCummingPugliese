import Vuex from 'vuex';
import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import index from '../pages/index.vue'

var localVue = createLocalVue();
localVue.use(Vuex);

var supermarkets_mock = [
    {
        address: null,
        id: 1,
        lat: 45.4640671,
        logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Italian_traffic_signs_-_icona_supermercato.svg/1024px-Italian_traffic_signs_-_icona_supermercato.svg.png",
        lon: 9.1553131,
        max_capacity: 1,
        mean_shopping_time: 10,
        name: "Supermarket1",
        timetable: '{"openingHour": "08:00:00", "closingHour": "20:00:00", "openingHourHoliday": "09:00:00", "closingHourHoliday": "18:00:00"}',
        waiting_time: 10
    },
    {
        address: null,
        id: 2,
        lat: 45.4640671,
        logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Italian_traffic_signs_-_icona_supermercato.svg/1024px-Italian_traffic_signs_-_icona_supermercato.svg.png",
        lon: 9.1553131,
        max_capacity: 1,
        mean_shopping_time: 10,
        name: "Supermarket2",
        timetable: '{"openingHour": "08:00:00", "closingHour": "20:00:00", "openingHourHoliday": "09:00:00", "closingHourHoliday": "18:00:00"}',
        waiting_time: 20
    },
    {
        address: null,
        id: 3,
        lat: 45.4640671,
        logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Italian_traffic_signs_-_icona_supermercato.svg/1024px-Italian_traffic_signs_-_icona_supermercato.svg.png",
        lon: 9.1553131,
        max_capacity: 1,
        mean_shopping_time: 10,
        name: "Supermarket3",
        timetable: '{"openingHour": "08:00:00", "closingHour": "20:00:00", "openingHourHoliday": "09:00:00", "closingHourHoliday": "18:00:00"}',
        waiting_time: 30
    }
    
]

// Example of testing only generated html
describe('index test', () => {
    // add this before each
    test('index page component methods', async () => {
        let actions;
        let store;
        let getters;
        getters = {
            "supermarket/selected_supermarket": jest.fn(() => {return supermarkets_mock[0]}),
            "supermarket/supermarket_list": jest.fn(() => {return supermarkets_mock}),
        }
        actions = {
            "auth/getToken": jest.fn(() => {return "token"}),
            "auth/getUsername": jest.fn(() => {return "user"}),
            "supermarket/setSupermarketList": jest.fn()
        };
        store = new Vuex.Store({
            state: {
                
            },
            actions
        });
        var wrapper = shallowMount(index, {
            localVue,
            store,
            mocks: {
                // Mocking the leaflet module
                $L: {
                    icon: () => ""
                }
            },
            data: function(){
                return {
                    supermarkets_list: supermarkets_mock,
                }
            },
            computed: {
                new_supermarkets_list(){
                    return supermarkets_mock
                }
            }
        });
        expect(wrapper.html()).toContain("map-container")

        wrapper.vm.showPopup("testing");
        expect(wrapper.vm.display_popup).toBe(true);

        wrapper.vm.hidePopup();
        expect(wrapper.vm.display_popup).toBe(false);

    })
})
