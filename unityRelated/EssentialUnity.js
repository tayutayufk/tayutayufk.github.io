function FitToDevice() {
    ua = window.navigator.userAgent.toLowerCase();
    if (ua.indexOf("android") !== -1 || ua.indexOf("ios") !== -1 || ua.indexOf("ipad") !== -1) {
        gameInstance.SendMessage("Main Camera", 'setSmartPhoneMode');
    }
}
function ManiRobot(func, motor, power) {
    var v = motor + "|" + power.toFixed();
    gameInstance.SendMessage('GameDirector', func, v);
}


//センサー情報取得
let SensorData;
let SensorName;
let Sensorflag;
function getValue(name) {
    Sensorflag = false;
    SensorName = name;

    if (name.indexOf("CS") != -1) {
        gameInstance.SendMessage('GameDirector', 'ReadCS', name);
    }
    if (name.indexOf("RF") != -1) {
        gameInstance.SendMessage('GameDirector', 'ReadRF', name);
    }


    let to = setTimeout(function () {
        Sensorflag = true;
    }, 500);
    while (!Sensorflag)
        clearTimeout(to);
    //console.log(SensorData);
    return SensorData;
}
function ReturnValueJS(data) {

    let strings = data.split('|');
    //console.log(data);
    if (strings[0] == SensorName) {
        Sensorflag = true;
        SensorData = Number(strings[1]);
    } else {
        //console.log(strings, SensorName);
        Sensorflag = true;
        SensorData = -1;
    }
}


//シーン、ミッション管理
let SceneName;
let SceneLoading;
let MissionState;
let mName;
let rName;
let pName;
function FetchSceneData() {
    let loc = window.location.href;

    if (loc.indexOf("mission") != -1) {
        SceneName = "Mission";
        gameInstance.SendMessage('GameDirector', 'MoveScene', 'Mission');

        var url = location.href;
        var params = url.split("?");
        params = params[1].split("&");

        mName = params[0];
        rName = params[1];
        pName = params[2];
        //mName = "basic_level4";
        //pName = "script";
    }
    if (loc.indexOf("craft") != -1) {
        SceneName = "Craft";
        gameInstance.SendMessage('GameDirector', 'MoveScene', 'Craft');
    }
    return SceneName;

}
function MissionLoad() {//ミッションシーンのロード前に呼ばれる
    SceneLoading = true;
    return mName;
}
function MissionCourseLoad() {
    if(!SceneLoading)return;
    SceneLoading = false;
    var StartShade = document.getElementById("shade");
    StartShade.style.display = "block";
}
function MissionStart() {
    if (SceneName == "Mission" && SceneLoading == false) {
        MissionState = true;
        var StartShade = document.getElementById("shade");
        StartShade.style.display = "none";
        var outputdisplay = document.getElementById("output");
        outputdisplay.style.display = "block";
        gameInstance.SendMessage('GameDirector', 'Move');
        runit(pName);
    }
}
function MissionFinish(str) {
    if(MissionState){
        MissionState = false;
        alert("Mission was " + str + "!");
        location.href = "index.html";
    }
    
}