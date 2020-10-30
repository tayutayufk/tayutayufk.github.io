var editorVue = new Vue({
    el: '#editorVue',
    data: {
        funcs: [
            {
                name: 'Robot.LED(name,mode)',
                cpfunc: 'cp(Robot.LED(,));',
                des: 'Function to operate LEDs. You have three LEDs.',
                parameters:[
                    {
                        name:"name",
                        type:"string",
                        des:"LED Name"
                    },
                    {
                        name:"mode",
                        type:"bool",
                        des:"True or False"
                    }
                ]
            },
        ]
    },
    template: `
    <div class="func" v-for="func in funcs">
    <a v-bind:onclick=func.cpfunc class="funcbtn">{{func.name}}</a>
    <p>{{func.des}}</p>
    <ul>
      <li v-for="parameter in parameters">{{parameter.name}} ({{parameter.type}}) : {{parameter.des}} </li>
    </ul>
  </div>`
})