window.onload = function() {
    if (navigator.userAgent.match(/iPhone|Android.+Mobile/)) {
        $(".icon").css({ 'width': '5vw', 'height': '5vw' });
    }
    return;
}

function onClickButton(func) {
    gameInstance.SendMessage('GameDirector', func);
}

function ManiRobot(func, motor, power) {
    var v = motor + "|" + power.toFixed();

    gameInstance.SendMessage('GameDirector', func, v);
}

function Hopup(str) {
    $('.contentHopup').text(str);
    $('.actHopup').fadeIn(300, function() {
        $('.actHopup').fadeOut(300);
    });
}