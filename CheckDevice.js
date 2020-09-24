document.write(window.navigator.userAgent+"\n");

ua = window.navigator.userAgent;
var Device = "PC";
if(ua.indexOf("android") !== -1 || ua.indexOf("ios") !== -1 || ua.indexOf("ipad") !== -1){
    Device = "SmatrPhone";
}
document.write(Device)