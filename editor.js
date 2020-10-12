var editor;
    require.config({ paths: { 'vs': 'node_modules/monaco-editor/min/vs' }});
    require(['vs/editor/editor.main'], function() {
        editor = monaco.editor.create(document.getElementById('container'), {
        value: [].join('\n'),
        language: 'python',
        fontSize: "20px"
    });
});

function SaveScript(){
    localStorage.setItem("script", editor.getValue());
}
function LoadScript(){
    editor.getModel().setValue(localStorage.getItem("script"));
}