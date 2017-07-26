// Komodo macro - shows all bookmarks in the Command Output tab
function get_all_bookmarks() {
  var bm = [];
  var views = ko.views.manager.getAllViews('editor');
  var bmask = 1 << ko.markers.MARKNUM_BOOKMARK;
  views.map(function(v) {
      var s = v.scimoz;
      var i = 0;
      while (true) {
        var res = s.markerNext(i, bmask);
        if (res > -1) {
            bm.push([v, res]);
            i = res + 1;
        } else {
            break;
        }
      }
  });
  var data = (bm.length ? bm.map(function(x) x[0].koDoc.displayPath + ":" + (x[1]+1)).join("\n") : "No bookmarks");
  return data;
}
  
function write_to_file(data) {
  var tmpFile = Components.classes["@mozilla.org/file/directory_service;1"].
                     getService(Components.interfaces.nsIProperties).
                     get("TmpD", Components.interfaces.nsIFile);
  tmpFile.append("koBookmarks.tmp");
  
  var file = Components.classes["@mozilla.org/file/local;1"].
                       createInstance(Components.interfaces.nsILocalFile);
  file.initWithPath(tmpFile.path);
  var foStream = Components.classes["@mozilla.org/network/file-output-stream;1"].
                           createInstance(Components.interfaces.nsIFileOutputStream);
  foStream.init(file, 0x02 | 0x08 | 0x20, 0666, 0); 
  var converter = Components.classes["@mozilla.org/intl/converter-output-stream;1"].
                            createInstance(Components.interfaces.nsIConverterOutputStream);
  converter.init(foStream, "UTF-8", 0, 0);
  converter.writeString(data);
  converter.close();
  var dataFile = tmpFile.path;
  return dataFile;
}

function parse_list(dataFile) {
  var osString = Components.classes["@mozilla.org/xre/app-info;1"]  
               .getService(Components.interfaces.nsIXULRuntime).OS;
  if (osString == "WINNT") {
    var echoCmd = "type ";
  }
  else {
    var echoCmd = "cat ";
  }
  
  ko.run.runEncodedCommand(window, echoCmd + dataFile +
    ' {"parseRegex": u"^(?P\<file\>.+?):(?P\<line\>\\d+)(?P\<content\>)$", \
    "showParsedOutputList": True, \
    "parseOutput": True}');
}

try {
  parse_list(write_to_file(get_all_bookmarks()));
} catch(ex) {
    alert("get_all_bookmarks failed: " + ex + "\n");
}
