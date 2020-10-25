var missionData = [];

window.onload = function(){
    for(key in localStorage){
        if(key == "MissionDataContainer"){
            var json = localStorage.getItem(key);
            missionData = JSON.parse( json );
        }
    }
}

function MDSave(){
    var json = JSON.stringify( missionData );
    localStorage.setItem("MissionDataContainer",json);
}
function SaveResult(mname,result,meta){
    for(i = 0;i < missionData.length;i++){
        if(missionData[i].name == mname){
            missionData[i].rlt = result;
            missionData[i].m = meta;
            MDSave();
            return;
        }
    }
    m = {name:mname,rlt:result,m:meta};
    missionData.push(m);
    MDSave();
    return;
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