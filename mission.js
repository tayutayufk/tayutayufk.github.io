var missionData = {};

window.onload = function(){
    for(key in localStorage){
        if(key == "MissionDataContainer"){
            missionData = localStorage.getItem(key);
        }
    }
}

function MDSave(){
    localStorage.setItem("MissionDataContainer",missionData);
}
function SaveResult(mname,result,meta){
    var m = {name:mname,result:result,meta:meta};
    missionData.push(m);
    MDSave();
}
function ReadResult(mname){
    for(m in missionData){
        if(m.name == mname){
            return m.result;
        }
    }
    m = {name:mname,result:"",meta:""};
    missionData.push(m);
}