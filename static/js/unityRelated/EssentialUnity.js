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
        gameInstance.SendMessage('GameDirector', 'ReadM', name);
    }


    let to = setTimeout(function() {
        Sensorflag = true;
    }, 500);
    while (!Sensorflag) {
        clearTimeout(to);
    }
    //console.log(SensorData);
    return SensorData;
}

function ReturnValueJS(data) {

    let strings = data.split('|');
    console.log(strings);
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
        mName = getParam("m");
    }
    if (loc.indexOf("craft") != -1) {
        SceneName = "Craft";
        gameInstance.SendMessage('GameDirector', 'MoveScene', 'Craft');

        rn = localStorage.getItem("lastRobot");
        rnd = localStorage.getItem("R_" + rn);
        //alert(rnd);
        setTimeout(function() {
            localStorage.setItem("robo3", rnd);
            $(".robotName").val(rn);
        }, 100);

        setTimeout(function() {
            onClickButton('ReLoad');
        }, 200);

        setTimeout(function() {
            onClickButton('LoadJson');
        }, 300);
    }
    return SceneName;

}

function MissionLoad() { //ミッションシーンのロード前に呼ばれる
    SceneLoading = true;
    return mName;
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
            $('.RltDes').text("Fall out!");

        }
        $('.ScoreWindow').show();

        SaveResult(mName, params[0], params[1], params[2]);
    }
}

function unityError(code) {
    alert(code)
}