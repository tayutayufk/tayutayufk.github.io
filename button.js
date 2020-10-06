function onClickButton(func){
    gameInstance.SendMessage('GameDirector',func);
}
function ManiRobot(func,motor,power){
    var v = motor + "|" + power.toFixed();

    gameInstance.SendMessage('GameDirector',func,v);
}