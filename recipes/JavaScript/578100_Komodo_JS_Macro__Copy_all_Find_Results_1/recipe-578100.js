/*******************************************************************************************************************
**      GetFindResults Macro
**      Purpose: Collect all current "Find (in Files)" results in Find Results tab 1
**                      into new (or reused) window for subsequent processing.
**      Author: Dave Wald
**      Date:   April, 2012
**      Notes:  Make sure there is a current Find Results window with lines of text in it,
**                      or it will just tell you it can't find anything to process.
**                      It only gets the "Find Results 1" pane now, but could easily be copied to do "Find Results 2" as well.
** 
*******************************************************************************************************************/
(function(){
  var columns;
  var curView;
  var newDocView;
  var targetView;
  var targetViewScimoz;
  var newText;
  var rowcnt = 0;
  var tab;
  var treeWidget;
  var viewMan = ko.views.manager;
  var findresMan = ko.findresults.getManager(1);
          //e.g. if exist "Find Results 1" tab, then parm is '1'
  var messages = get_messages();
  var FindResultsOutputBuffer = [];
  var reuseOutputView = true;
  //  Set this to false to send output to a new view each time.
  //      If you are reusing the view, don't save it to disk or the
  //      viewMan.getUntitledView("Find Results") function won't be able to find it. 
  //  If you are finished searching for a while, or just really want to save
  //      that particular view to disk,   go ahead. It will then just create a new one,
  //      and then start reusing the new one as long as it remains unsaved.
  
  try {
    curView = findresMan.view;
    treeWidget = findresMan.doc.getElementById("findresults");
    columns = treeWidget.columns;
    rowcnt = curView.rowCount;
    if (rowcnt === 0) {
      throw new Error("rowcnt is 0");
    }
  }
  catch(ex){
    error_notify(ex);
    return false;
  }
  if (reuseOutputView){
    targetView = viewMan.getUntitledView("Find Results");
  } else {
    targetView = null;
  }
  if (targetView == null){
    targetView = viewMan._doNewView(null, null);
    targetView.koDoc.baseName = "Find Results";
    tab = targetView.parentNode._tab;
    tab.label = tab.tooltipText = "Find Results";
  }
  for (var i = 0; i < rowcnt; i++){ //see Treeview.js for usage
    FindResultsOutputBuffer.push (curView.getCellText(i, columns[0]) + " | "
                                + curView.getCellText(i, columns[1]) + " | "
                                + curView.getCellText(i, columns[2]) ) ;        
  }
  targetViewScimoz = targetView.scimoz;
  targetViewScimoz.selectAll();
  targetViewScimoz.clear();
  targetViewScimoz.addText(84, "************************** Find Results *******************************************\n");
  newText = FindResultsOutputBuffer.join('\n')
  targetViewScimoz.addText(newText.length, newText);
  
  return true;

  //support functions
  function get_messages () {
    var msgs = {
        m0:"Unknown error.",
        m1:"Could not get Find Results Manager. Make sure you have a Find Results tab in one of the panes.",
        m2:"Could not get results view.",
        m3:"Could not find any results. Make sure your Find Results tab has rows in it.",
        m4:"Could not find any columns with data. Make sure your Find Results tab has rows and columns with data in it.",
        m5:"Could not find any result rows. Make sure your Find Results tab has at least one row with data in it."
        }
    return msgs;
  }
  function error_notify(ex){
    var title = "Get Find Results";
    var messages = get_messages();
    var message = messages.m0;
    if (!findresMan) {
      message = messages.m1;  
    }
    else if (!curView){
      message = messages.m2;
    }
    else if (!treeWidget){
      message = messages.m3;
    }
    else if (!(columns) || columns.count === 0){
      message = messages.m4;  
    }
    else if (!(rowcnt) || rowcnt < 1){
      message = messages.m5;
    }
    else {
      message = ex.message;
    }
    new ko.dialogs.alert(message, null, title);
  }
})();
