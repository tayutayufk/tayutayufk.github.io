document.write(window.navigator.userAgent.toLowerCase());

ua = window.navigator.userAgent.toLowerCase();
var Device = "PC";
if(ua.indexOf("android") !== -1 || ua.indexOf("ios") !== -1 || ua.indexOf("ipad") !== -1){
    Device = "SmartPhone";
}else{
    Device = "PC";
}
document.write(Device)