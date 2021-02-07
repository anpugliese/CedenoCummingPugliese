import Vuex from 'vuex';
import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import booking from '../pages/booking.vue'

var localVue = createLocalVue();
localVue.use(Vuex);

var supermarket_mock = 
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
    }


// Example of testing only generated html
describe('booking page test', () => {
    // add this before each
    test('booking page testing', async () => {
        let actions;
        let store;
        let getters;
        getters = {
            "auth/getUsername": jest.fn(() => {return "username"}),
            "supermarket/getSelectedSupermarket": jest.fn(() => {return supermarket_mock}),
            "supermarket/getSupermarketList": jest.fn(() => {return [supermarket_mock, supermarket_mock, supermarket_mock]}),
        }
        actions = {
            "auth/getToken": jest.fn(() => {return "token"}),
            "auth/getUsername": jest.fn(() => {return "user"}),
            "supermarket/setSupermarketList": jest.fn(),
            "supermarket/setSelectedSupermarket": jest.fn(),
        };
        store = new Vuex.Store({
            state: {
                
            },
            actions,
            getters,
        });
        var wrapper = shallowMount(booking, {
            localVue,
            store,
            mocks: {
            },
            data: function(){
                return {
                    selected_supermarket_name: supermarket_mock.name,
                }
            },
        });
        expect(wrapper.html()).toContain("Booking " + wrapper.vm.selected_supermarket_name);

    })
})
