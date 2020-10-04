function onClickButton(arg){
    gameInstance.SendMessage('GameDirector',arg);
}
function ManiRobot(arg,motor,power){
    gameInstance.SendMessage('GameDirector',arg,motor,power);
}