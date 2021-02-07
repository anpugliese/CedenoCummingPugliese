import Vuex from 'vuex';
import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import list from '../pages/list.vue'

var localVue = createLocalVue();
localVue.use(Vuex);

var supermarket_mock = [
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
        waiting_time: 20
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
        waiting_time: 10
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

var supermarket_mock2 = [
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
        waiting_time: 20
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
        waiting_time: 10
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

/**
 * Assert that the view contains the name of the 1rst supermarket in supermarkets_list
 * Order a mock supermarkets list and compare that it is different to itself before ordering 
 */
describe('list page test', () => {
    test('list page testing', async () => {
        let actions;
        let store;
        let getters;
        getters = {
            "auth/getUsername": jest.fn(() => {return "username"}),
            "supermarket/getSelectedSupermarket": jest.fn(() => {return supermarket_mock[0]}),
            "supermarket/getSupermarketList": jest.fn(() => {return supermarket_mock}),
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
        var wrapper = shallowMount(list, {
            localVue,
            store,
            mocks: {
            },
            data: function(){
                return {
                    selected_supermarket_name: supermarket_mock.name,
                    supermarket_list: supermarket_mock,
                    supermarket_list_not_ordered: supermarket_mock2,
                }
            },
        });
        expect(wrapper.html()).toContain(wrapper.vm.supermarket_list[0].name);
        wrapper.setData({
            supermarket_list: supermarket_mock,
            supermarket_list_not_ordered: supermarket_mock2
        });
        expect(wrapper.vm.sortList(wrapper.vm.supermarket_list) != wrapper.vm.supermarket_list_not_ordered).toBe(true);

    })
})
