const app = new Vue({
  el: '#app',
  data: {
    showFilter: false,
    filter:{
      gender:'',
      meals:'',
    },
    rooms: [{
      id: 1,
      title: 'room 1',
      duration: '3 months',
      vacancy: 4,
      gender: {
        male: true,
        female: false,
      },
      food: true,
      imgs: [
        'http://placekitten.com/300/200',
        'http://placekitten.com/300/201',
        'http://placekitten.com/300/202',
        'http://placekitten.com/300/203',
        'http://placekitten.com/300/204',
        'http://placekitten.com/300/205',
      ],
    },{
      id: 2,
      title: 'room 2',
      duration: '5 months',
      gender: {
        female: true,
      },
      imgs: [
        'http://placekitten.com/300/204',
        'http://placekitten.com/300/201',
        'http://placekitten.com/300/202',
        'http://placekitten.com/300/203',
        'http://placekitten.com/300/204',
        'http://placekitten.com/300/205',
      ],
    }]
  },
  components: {
    v_room: window.vRoom,
  }
});
