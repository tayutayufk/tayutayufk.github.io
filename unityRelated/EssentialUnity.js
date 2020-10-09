function  FitToDevice(){
    ua = window.navigator.userAgent.toLowerCase();
    if(ua.indexOf("android") !== -1 || ua.indexOf("ios") !== -1 || ua.indexOf("ipad") !== -1){
        gameInstance.SendMessage("Main Camera", 'setSmartPhoneMode');
    }
}
function ManiRobot(func,motor,power){
    var v = motor + "|" + power.toFixed();
    gameInstance.SendMessage('GameDirector',func,v);
}

let SensorData;
let SensorName;
let Sensorflag;

function getValue(name){
    Sensorflag = false;
    SensorName = name;
    
    if(name.indexOf("CS") != -1){
        //console.log("CS");
        gameInstance.SendMessage('GameDirector','ReadCS',name);
    }
    if(name.indexOf("RF") != -1){
        //console.log("RF");
        gameInstance.SendMessage('GameDirector','ReadRF',name);
    }

    
    let to = setTimeout(function(){
        Sensorflag = true;
    },500);
    while(!Sensorflag)
    clearTimeout(to);
    console.log(SensorData);
    return SensorData;
}
function ReturnValueJS(data){
    
    let strings = data.split('|');
    //console.log(data);
    if(strings[0] == SensorName){
        Sensorflag = true;
        SensorData = Number(strings[1]);
    }else{
        Sensorflag = true;
        SensorData = -1;
    }
}