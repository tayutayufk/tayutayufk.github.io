var initText = [
    'import Robot',
    'from time import sleep'
].join('\n');
var editor;
require.config({ paths: { 'vs': 'static/js/node_modules/monaco-editor/min/vs' } });
require(['vs/editor/editor.main'], function() {
    editor = monaco.editor.create(document.getElementById('container'), {
        value: initText,
        language: 'python',
        fontSize: "15%"
    });
});



function LoadScript(pName) {
    editor.getModel().setValue(localStorage.getItem("S_" + pName));
}

function setText(code) {
    initText = code;
}

function cp(string) {
    var tmp = document.createElement("div");
    var pre = document.createElement('pre');

    pre.style.webkitUserSelect = 'auto';
    pre.style.userSelect = 'auto';

    tmp.appendChild(pre).textContent = string;

    var s = tmp.style;
    s.position = 'fixed';
    s.right = '200%';

    document.body.appendChild(tmp);
    document.getSelection().selectAllChildren(tmp);

    var result = document.execCommand("copy");
    document.body.removeChild(tmp);

    return result;
}