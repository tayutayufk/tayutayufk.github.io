ua = window.navigator.userAgent.toLowerCase();
var Device = "PC";
if(ua.indexOf("android") !== -1 || ua.indexOf("ios") !== -1 || ua.indexOf("ipad") !== -1){
    Device = "SmartPhone";
    unityInstance.SendMessage('Main Camera', 'setSmartPhoneMode')
}else{
    Device = "Desktop";
    gameInstance.SendMessage("MainCamera",  'setSmartPhoneMode')
}
document.write(Device)