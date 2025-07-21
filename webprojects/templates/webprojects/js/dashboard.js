// Future: Add theme toggle, shortcut keys, etc.
console.log("CodeThinkers dashboard ready.");
var editor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
  lineNumbers: true,
  mode: 'htmlmixed',
  theme: 'monokai',
  tabSize: 2,
  indentUnit: 2,
  lineWrapping: true,
  autoCloseTags: true,
  autoCloseBrackets: true,
  matchBrackets: true,
  showCursorWhenSelecting: true,
  extraKeys: {
    'Ctrl-Space': 'autocomplete',
    'Ctrl-S': function(cm) {
      cm.save();
      alert('File saved!');
    }
  }
});
