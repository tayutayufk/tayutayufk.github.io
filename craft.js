Vue.component('part_illust', {
    props: ['image-dir', 'disc'],
    templete: `
        <input class="partimage" v-bind:src="image-dir" type="image" @click="select">
        <h1>takayasu<h1>
        `,
    methods: {
        select: function () {
            //onClickButton(this.disc);
        }
    },

});

var appGeneral = new Vue({
    el:'#appGeneral',
    data:{
        parts: [
            { imagedir:"unityRelated/PartImage/BB.png",disc:"Basic Block"},
            { imagedir:"unityRelated/PartImage/TB.png",disc:"Tire Bid"},
            { imagedir:"unityRelated/PartImage/TM.png",disc:"Tire mini"}
        ]
    }
});
Vue.component('bigTakayasu',{
    data(){
        return{
            msg:"takayasu"
        }
    },
    templete:'<h1>{{msg}}</h1>'
});