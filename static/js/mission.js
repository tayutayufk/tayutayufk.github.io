let missionData = {};

var j = localStorage.getItem("MissionDataContainer");
if (j) {
    missionData = JSON.parse(j);
}


function MDLoad() {
    var json = localStorage.getItem("MissionDataContainer");
    if (json) { missionData = JSON.parse(json); }
}

function MDSave() {
    var json = JSON.stringify(missionData);
    localStorage.setItem("MissionDataContainer", json);
}

function SaveResult(mname, result, time, meta) {
    MDLoad();
    if (missionData) {
        if (mname in missionData) {
            m = missionData[mname];

            if (result == "clear") {
                if (m["rlt"] == "clear" && Number(m["time"]) < Number(time)) {
                    m["time"] = time
                    m["m"] = meta
                    missionData[mname] = m
                    MDSave();
                    return;
                } else {
                    m["rlt"] = result;
                    m["time"] = time
                    m["m"] = meta
                    missionData[mname] = m
                    MDSave();
                    return;
                }
            }
        } else {
            missionData[mname] = { "rlt": result, "time": time, "m": meta };
            MDSave();
            return;
        }
    } else {
        missionData[mname] = { "rlt": result, "time": time, "m": meta };
        MDSave();
        return;
    }
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