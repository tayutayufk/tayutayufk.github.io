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

    if (name.indexOf("CS_") != -1) {
        name = name.slice(3);
        SensorName = name;
        gameInstance.SendMessage('GameDirector', 'ReadCS', name);
    } else if (name.indexOf("RF_") != -1) {
        name = name.slice(3);
        SensorName = name;
        gameInstance.SendMessage('GameDirector', 'ReadRF', name);
    } else if (name.indexOf("M_") != -1) {
        name = name.slice(2);
        SensorName = name;
        gameInstance.SendMessage('GameDirector', 'RotaryEncoder', name);
    } else if (name.indexOf("GP_") != -1) {
        name = name.slice(3);
        SensorName = name;
        gameInstance.SendMessage('GameDirector', 'GyroSensor', name);
    } else if (name.indexOf("GV_") != -1) {
        name = name.slice(3);
        SensorName = name;
        gameInstance.SendMessage('GameDirector', 'GyroSensor', name);
    }


    let to = setTimeout(function() {
        Sensorflag = true;
    }, 500);
    while (!Sensorflag) {
        clearTimeout(to);
    }
    //console.log(SensorData);
    if (name.indexOf("GP_") != -1) {
        return
    } else if (name.indexOf("GV_") != -1) {
        name = name.slice(3);
        SensorName = name;
        gameInstance.SendMessage('GameDirector', 'GyroSensor', name);
    }
    return SensorData;
}

function ReturnValueJS(data) {

    let strings = data.split('|');

    if (strings[0] == SensorName) {
        Sensorflag = true;
        if (strings.length > 2) {
            SensorData = {
                'x': parseFloat(strings[1]),
                'y': parseFloat(strings[2]),
                'z': parseFloat(strings[3]),
                'ax': parseFloat(strings[4]),
                'ay': parseFloat(strings[5]),
                'az': parseFloat(strings[6]),
                'vx': parseFloat(strings[7]),
                'vy': parseFloat(strings[8]),
                'vz': parseFloat(strings[9]),
                'avx': parseFloat(strings[10]),
                'avy': parseFloat(strings[11]),
                'avz': parseFloat(strings[12])
            }
        } else {
            SensorData = Number(strings[1]);
        }
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
        mName = getParam("m");
        localStorage.setItem("lastMission", mName);
    }
    if (loc.indexOf("craft") != -1) {
        SceneName = "Craft";
        gameInstance.SendMessage('GameDirector', 'MoveScene', 'Craft');
    }
    return SceneName;

}

function MissionLoad() {
    SceneLoading = true;
    return mName;
}

function CraftLoad() {
    rn = localStorage.getItem("lastRobot");
    rnd = localStorage.getItem("R_" + rn);
    if (!rnd) {
        return;
    }
    localStorage.setItem("robo3", rnd);
    $(".robotName").val(rn);
    setTimeout(function() {
        onClickButton('LoadJson');
    }, 300);
}

function MissionCourseLoad(str) {
    if (!SceneLoading) return;
    SceneLoading = false;
    var StartShade = document.getElementById("shade");
    StartShade.style.display = "block";
}

function MissionStart() {
    if (SceneName == "Mission" && SceneLoading == false) {
        MissionState = true;
        var StartShade = document.getElementById("shade");
        StartShade.style.display = "none";
        displayBtn();
        gameInstance.SendMessage('GameDirector', 'Move');
        runit();
    }

}

function MissionFinish(str) {
    if (MissionState) {
        MissionState = false;
        var params = str.split("|");
        if (params[0] == "clear") {
            $('.result').text("Clear!");
            $('.RltDes').text("Congratulations!");

        } else {
            $('.result').text("Faild");
            $('.RltDes').text("Fall out.");
            $('.result').css({ 'color': 'red' })
        }

        if (params) {
            $('.RltTime').text("Time : " + params[1]);


        }
        $('.ScoreWindow').show();

        SaveResult(mName, params[0], params[1], params[2]);
    }
}

function unityError(code) {
    alert(code)
}