var pastebin = {
    post : function() {
        var selection = ko.views.manager.currentView.selection;
        
        if (selection == "") {
            ko.dialogs.alert("No selection found");
            return;
        }
        
        var lang = encodeURIComponent(this.ko2pastebinLanguage());
        var text = encodeURIComponent(selection);
        var email = encodeURIComponent("me@mail.com");
        var nick = encodeURIComponent("me");
        var expiry = encodeURIComponent("1D"); // N = Never, 10M = 10 Minutes, 1H = 1 Hour, 1D = 1 Day, 1M = 1 Month
        
        var httpReq = new XMLHttpRequest();
        httpReq.open("post", "http://pastebin.com/api_public.php", false);
        httpReq.setRequestHeader("content-type",
                                 "application/x-www-form-urlencoded");

        var requestString = "paste_private=1&paste_format={1}&paste_code={2}&paste_email={3}&paste_name={4}&paste_expire_date={5}";
        var sendString = requestString
                            .replace("{1}", lang)
                            .replace("{2}", text)
                            .replace("{3}", email)
                            .replace("{4}", nick)
                            .replace("{5}", expiry);
        httpReq.setRequestHeader("Content-length", sendString.length);
        httpReq.send(sendString);

        var url = this.getReturnURL(httpReq);
        httpReq.setRequestHeader("Connection", "close");
        this.copyText(url);
        ko.statusBar.AddMessage("Url " + url
                                + " copied on clipboard using lang " + lang,
                                "pastebin_macro", 3000, true)
        ko.browse.openUrlInDefaultBrowser(url);
    },
    
    getReturnURL : function(httpReq) {
        return httpReq.responseText;
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
        langMap["Assembler"] = "asm";
        langMap["Bash"] = "bash";
        langMap["C++"] = "c";
        langMap["C++"] = "cpp";
        langMap["CSS"] = "css";
        langMap["Diff"] = "diff";
        langMap["Eiffel"] = "eiffel";
        langMap["Fortran"] = "fortran";
        langMap["FreeBasic"] = "freebasic";
        langMap["HTML"] = "html4strict";
        langMap["Java"] = "java";
        langMap["JavaScript"] = "javascript";
        langMap["Lisp"] = "lisp";
        langMap["Lua"] = "lua";
        langMap["Matlab"] = "matlab";
        langMap["SQL"] = "mysql";
        langMap["Nsis"] = "nsis";
        langMap["PL-SQL"] = "oracle8";
        langMap["Pascal"] = "pascal";
        langMap["Perl"] = "perl";
        langMap["PHP"] = "php";
        langMap["Python"] = "python";
        langMap["Ruby"] = "ruby";
        langMap["Scheme"] = "scheme";
        langMap["Smarty"] = "smarty";
        langMap["SQL"] = "sql";
        langMap["Tcl"] = "tcl";
        langMap["VisualBasic"] = "vb";
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
pastebin.post();
