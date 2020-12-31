window.onload = function() {
    if (navigator.userAgent.match(/|ios|ipad|iPad|iPhone|Android.+Mobile/)) {
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

function getParam(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}