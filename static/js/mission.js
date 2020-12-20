let missionData = [];

var j = localStorage.getItem("MissionDataContainer");
if (j) {
    missionData = JSON.parse(j);
}


function MDLoad() {
    var json = localStorage.getItem("MissionDataContainer");
    missionData = JSON.parse(json);
}

function MDSave() {
    var json = JSON.stringify(missionData);
    localStorage.setItem("MissionDataContainer", json);
}

function SaveResult(mname, result, time, meta) {
    MDLoad();
    for (i = 0; i < missionData.length; i++) {
        if (missionData[i].name == mname) {
            if (missionData[i].rlt == "faild") {
                missionData[i].rlt = result;
                missionData[i].time = time;
                missionData[i].m = meta;
            } else if (result == "clear") {
                if (Number(missionData[i].time) < Number(time)) {
                    missionData[i].time = time;
                    missionData[i].m = meta;
                }
            }
            MDSave();
            return;
        }
    }
    m = { "name": mname, "rlt": result, "time": time, "m": meta };
    missionData.push(m);
    MDSave();
    return;
}

function ReadResult(mname) {
    for (m in missionData) {
        if (m.name == mname) {
            return m;
        }
    }
    return "";
}