komodo.assertMacroVersion(3);
if (komodo.view) { komodo.view.setFocus(); }
ko.commands.doCommand('cmd_lineDuplicate')
ko.commands.doCommand('cmd_end')
ko.commands.doCommand('cmd_lineNext')
ko.commands.doCommand('cmd_left')
ko.commands.doCommand('cmd_selectWordLeft')

// Skip the code above if you dont whant the script to insert a new line. It will then simply convert the selected value to rem. Select 12px and it will be converted to 0,75rem. 

var koedit = ko.views.manager.currentView.scimoz;

    if ( !!koedit.selText ) {
        var newText = koedit.selText;
        
        var rem_base = 16; //Replace the value here to the rem base you have in your own CSS file!
        
        newText = newText.replace("px", ""); // Removes the px prefix
        newText = parseInt(newText); //Convert the string to a int 
        newText = newText / rem_base; //Convert to rem value
        newText = newText.toFixed(9); //Shorten the rem value to 9 decimals 
        
        koedit.replaceSel( newText + "rem" ); //Return the new value with a rem prefix
    }
