function onBB(){
    gameInstance.SendMessage('GameDirector','BB');
}
function onMB(){
    gameInstance.SendMessage('GameDirector','MB');
}
function onMN(){
    gameInstance.SendMessage('GameDirector','MN');
}
function onMM(){
    gameInstance.SendMessage('GameDirector','MM');
}
function onTM(){
    gameInstance.SendMessage('GameDirector','TM');
}
function onTB(){
    gameInstance.SendMessage('GameDirector','TB');
}
function onRemove(){
    gameInstance.SendMessage('GameDirector','Remove');
}

function onSave(){
    gameInstance.SendMessage('GameDirector','SaveJson');
}
function onLoad(){
    gameInstance.SendMessage('GameDirector','LoadJson');
}
function GoMission(){
    gameInstance.SendMessage('GameDirector','GoMission');
}