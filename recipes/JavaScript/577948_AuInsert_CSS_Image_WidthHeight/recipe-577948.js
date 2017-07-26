var view = ko.views.manager.currentView;
var scimoz = view.scimoz;
var currentPos = scimoz.currentPos;
var currentLine = scimoz.lineFromPosition(currentPos);
var lineStartPos = scimoz.positionFromLine(currentLine);
var lineEndPos = scimoz.getLineEndPosition(currentLine);
var text = scimoz.getTextRange(lineStartPos, lineEndPos);
if (/.*url.*\(["']?(.+?)["']?\)/.test(text)) {
    var url = RegExp.$1;
    var currentView = ko.views.manager.currentView;
    var cwd = currentView.document.file.dirName;
    var prefix = (text.indexOf("http") == -1)? "file:///" + cwd + "/" : "";
    url = prefix + url;
    
    var img = new Image();
    img.src = url;

    // Try 10 times
    var lim = 10;
    var i = 0;
    var writeTag = function(i) {
        if (i >= lim) {
            ko.dialogs.alert("Sorry, can't find the height and width of the image");
        } else if (!img.height || !img.width) {
            ko.statusBar.AddMessage("No img info at attempt " + i, "editor", 500, true);
            setTimeout(writeTag, 100, i + 1);
        } else {
            var newText = ('\r\n\theight: ' + img.height + 'px;' +
                           '\r\n\twidth: ' + img.width + 'px;');
            
            scimoz.lineEnd();
            scimoz.insertText(lineEndPos, newText);
        }
    }
    writeTag(0);
} else {
    alert("Can't get image info from URL '" + text + '"');
}

// TESTING:  Put the cursor somewhere on one of the following lines, run the macro.
// background: url(http://upload.wikimedia.org/wikipedia/commons/thumb/0/04/WhiteandKeynes....) 0 0 no-repeat;  /* ABSOLUTE FILE PATH */
// background: url(../images/bgtile.jpg) 0 0 no-repeat;    /* RELATIVE FILE PATH */
