ua = window.navigator.userAgent.toLowerCase();
var Device = "PC";
if(ua.indexOf("android") !== -1 || ua.indexOf("ios") !== -1 || ua.indexOf("ipad") !== -1){
    Device = "SmartPhone";
    //gameInstance.SendMessage("MainCamera", 'setSmartPhoneMode')
}else{
    Device = "Desktop";
    //gameInstance.SendMessage("MainCamera",  'setSmartPhoneMode')
}
document.write(Device)

function  FitToDevice(){
    target = document.getElementById("Device");
    target.innerHTML = window.navigator.userAgent.toLowerCase();
    //gameInstance.SendMessage("Main Camera", 'setSmartPhoneMode');
    //document.write("FUCK");
    //unityInstance.SendMessage("Main Camera", 'setSmartPhoneMode')
    ua = window.navigator.userAgent.toLowerCase();
    if(ua.indexOf("android") !== -1 || ua.indexOf("ios") !== -1 || ua.indexOf("ipad") !== -1){
        gameInstance.SendMessage("MainCamera", 'setSmartPhoneMode')
    }
}