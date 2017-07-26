var pastebin = {
    post : function() {
        var selection = ko.views.manager.currentView.selection;
        
        if (selection == "") {
            ko.dialogs.alert("No selection found");
            return;
        }
        
        var lang = encodeURIComponent(this.ko2pastebinLanguage());
        var text = encodeURIComponent(selection);
        var nick = encodeURIComponent("anonymous");
        var expiry = encodeURIComponent("d");
        
        var httpReq = new XMLHttpRequest();
        httpReq.open("post", "http://pastebin.mozilla.org", false);
        httpReq.setRequestHeader("content-type",
                                 "application/x-www-form-urlencoded");

        var requestString = "parent_pid=&format={1}&code2={2}&poster={3}&paste=Send&expiry={4}";
        var sendString = requestString
                            .replace("{1}", lang)
                            .replace("{2}", text)
                            .replace("{3}", nick)
                            .replace("{4}", expiry);
        httpReq.send(sendString);

        var url = this.getReturnURL(httpReq);
        this.copyText(url);
        ko.statusBar.AddMessage("Url " + url
                                + " copied on clipboard using lang " + lang,
                                "pastebin_macro", 3000, true)
    },
    
    getReturnURL : function(httpReq) {
        return "http://pastebin.mozilla.org/"
            + httpReq.responseText.match('name="parent_pid" value="(.*)"')[1];
    },
    
    copyText : function(str) {
        Components.classes["@mozilla.org/widget/clipboardhelper;1"]
            .getService(Components.interfaces.nsIClipboardHelper)
            .copyString(str); 
    },
    
    ko2pastebinLanguage : function() {
        var langMap = {};

        langMap["Text"] = "text";
        langMap["ActionScript"] = "actionscript";
        langMap["Ada"] = "ada";
        langMap["Apache"] = "apache";
        //langMap[""] = "applescript";
        langMap["Assembler"] = "asm";
        //langMap[""] = "asp";
        langMap["Bash"] = "bash";
        langMap["C++"] = "c";
        //langMap[""] = "c_mac";
        //langMap[""] = "caddcl";
        //langMap[""] = "cadlisp";
        langMap["C++"] = "cpp";
        //langMap[""] = "csharp";
        //langMap[""] = "cfm";
        langMap["CSS"] = "css";
        //langMap[""] = "d";
        //langMap[""] = "delphi";
        langMap["Diff"] = "diff";
        //langMap[""] = "dos";
        langMap["Eiffel"] = "eiffel";
        langMap["Fortran"] = "fortran";
        langMap["FreeBasic"] = "freebasic";
        //langMap[""] = "gml";
        langMap["HTML"] = "html4strict";
        //langMap[""] = "ini";
        langMap["Java"] = "java";
        langMap["JavaScript"] = "javascript";
        langMap["Lisp"] = "lisp";
        langMap["Lua"] = "lua";
        langMap["Matlab"] = "matlab";
        //langMap[""] = "mpasm";
        langMap["SQL"] = "mysql";
        langMap["Nsis"] = "nsis";
        //langMap[""] = "objc";
        //langMap[""] = "ocaml";
        //langMap[""] = "oobas";
        langMap["PL-SQL"] = "oracle8";
        langMap["Pascal"] = "pascal";
        langMap["Perl"] = "perl";
        langMap["PHP"] = "php";
        langMap["Python"] = "python";
        //langMap[""] = "qbasic";
        //langMap[""] = "robots";
        langMap["Ruby"] = "ruby";
        langMap["Scheme"] = "scheme";
        langMap["Smarty"] = "smarty";
        langMap["SQL"] = "sql";
        langMap["Tcl"] = "tcl";
        langMap["VisualBasic"] = "vb";
        //langMap[""] = "vbnet";
        //langMap[""] = "visualfoxpro";
        langMap["XBL"] = "xml";
        langMap["XML"] = "xml";
        langMap["XSLT"] = "xml";
        langMap["XUL"] = "xml";

        language = langMap[ko.views.manager.currentView.document.language];
        if (language == undefined) {
            return "text";
        }
        return language;
    }

};

function printKomodoLanguages() {
    append_to_command_output_window("", true);
    function printLang(hierarchy) {
        var children = new Object();
        var count = new Object();
    
        if (hierarchy.container == true)  {
            hierarchy.getChildren(children, count);
            children = children.value;
    
            for (i = 0; i < children.length; i++)  {
                printLang(children[i]);
            }
        } else {
            append_to_command_output_window(hierarchy.name);
        }
    }

    var langService = Components.classes["@activestate.com/koLanguageRegistryService;1"]
                .getService(Components.interfaces.koILanguageRegistryService);
    printLang(langService.getLanguageHierarchy());

}

pastebin.post();
