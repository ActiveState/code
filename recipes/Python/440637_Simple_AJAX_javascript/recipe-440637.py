this is ajax.html
------------------------------------------------
<html>
<head>
<title>simple ajax json example</title>
<script language="JavaScript">
    //json parser
    //from json.org with small modification
    var cur_str_chr;
    function json_parse(text) {
        var at = 0;
        var ch = ' ';

        function error(m) {
            throw {
                name: 'JSONError',
                message: m,
                at: at - 1,
                text: text
            };
        }

        function next() {
            ch = text.charAt(at);
            at += 1;
            return ch;
        }

        function white() {
            while (ch !== '' && ch <= ' ') {
                next();
            }
        }

        function str() {
            var i, s = '', t, u;

            if (ch == '\'' || ch == '"') { //change " to ' for python
                cur_str_chr = ch;
outer:          while (next()) {
                    if (ch == cur_str_chr) {
                        next();
                        return s;
                    } else if (ch == '\\') {
                        switch (next()) {
                        case 'b':
                            s += '\b';
                            break;
                        case 'f':
                            s += '\f';
                            break;
                        case 'n':
                            s += '\n';
                            break;
                        case 'r':
                            s += '\r';
                            break;
                        case 't':
                            s += '\t';
                            break;
                        case 'u':
                            u = 0;
                            for (i = 0; i < 4; i += 1) {
                                t = parseInt(next(), 16);
                                if (!isFinite(t)) {
                                    break outer;
                                }
                                u = u * 16 + t;
                            }
                            s += String.fromCharCode(u);
                            break;
                        default:
                            s += ch;
                        }
                    } else {
                        s += ch;
                    }
                }
            }
            error("Bad string");
        }

        function arr() {
            var a = [];

            if (ch == '[') {
                next();
                white();
                if (ch == ']') {
                    next();
                    return a;
                }
                while (ch) {
                    a.push(val());
                    white();
                    if (ch == ']') {
                        next();
                        return a;
                    } else if (ch != ',') {
                        break;
                    }
                    next();
                    white();
                }
            }
            error("Bad array");
        }

        function obj() {
            var k, o = {};

            if (ch == '{') {
                next();
                white();
                if (ch == '}') {
                    next();
                    return o;
                }
                while (ch) {
                    k = str();
                    white();
                    if (ch != ':') {
                        break;
                    }
                    next();
                    o[k] = val();
                    white();
                    if (ch == '}') {
                        next();
                        return o;
                    } else if (ch != ',') {
                        break;
                    }
                    next();
                    white();
                }
            }
            error("Bad object");
        }

        function num() {
            var n = '', v;
            if (ch == '-') {
                n = '-';
                next();
            }
            while (ch >= '0' && ch <= '9') {
                n += ch;
                next();
            }
            if (ch == '.') {
                n += '.';
                while (next() && ch >= '0' && ch <= '9') {
                    n += ch;
                }
            }
            if (ch == 'e' || ch == 'E') {
                n += 'e';
                next();
                if (ch == '-' || ch == '+') {
                    n += ch;
                    next();
                }
                while (ch >= '0' && ch <= '9') {
                    n += ch;
                    next();
                }
            }
            if (ch == 'L')next();//for python long
            v = +n;
            if (!isFinite(v)) {
                error("Bad number");
            } else {
                return v;
            }
        }

        function word() {
            switch (ch) {
                case 't':
                    if (next() == 'r' && next() == 'u' && next() == 'e') {
                        next();
                        return true;
                    }
                    break;
                case 'f':
                    if (next() == 'a' && next() == 'l' && next() == 's' &&
                            next() == 'e') {
                        next();
                        return false;
                    }
                    break;
                case 'n':
                    if (next() == 'u' && next() == 'l' && next() == 'l') {
                        next();
                        return null;
                    }
                    break;
            }
            error("Syntax error");
        }

        function val() {
            white();
            switch (ch) {
                case '{':
                    return obj();
                case '[':
                    return arr();
                case '\'':
                case '"':
                    return str();
                case '-':
                    return num();
                default:
                    return ch >= '0' && ch <= '9' ? num() : word();
            }
        }

        return val();
    }
    //end json parser

function loadurl(dest) { 
    xmlhttp = window.XMLHttpRequest?new XMLHttpRequest(): new ActiveXObject("Microsoft.XMLHTTP");
    xmlhttp.onreadystatechange = pop_table;
    xmlhttp.open("GET", dest);
    xmlhttp.setRequestHeader("If-Modified-Since", "Sat, 1 Jan 2000 00:00:00 GMT");
    xmlhttp.send(null);
}
function pop_table() {
    if ((xmlhttp.readyState == 4) && (xmlhttp.status == 200)) {
        var json_data = json_parse(xmlhttp.responseText);
	var rows = document.getElementById("testtable").getElementsByTagName("tr");
	rows[0].childNodes[0].innerHTML = json_data[0]['one']
	rows[0].childNodes[1].innerHTML = json_data[0]['two']
	rows[0].childNodes[2].innerHTML = json_data[0]['three']
	for(i=0;i<rows[1].childNodes.length;i++)
		rows[1].childNodes[i].innerHTML = json_data[1][i]
	rows[2].childNodes[0].innerHTML = json_data[2]['title']
	rows[2].childNodes[2].innerHTML = json_data[2]['random']
    }
}
</script>
</head>
<body>
<div id="clickhere" onclick="loadurl('/cgi-bin/ajax.cgi')">click here</div>
<table id="testtable" border=1>
<tr><td>11</td><td>12</td><td>13</td></tr>
<tr><td>21</td><td>22</td><td>23</td></tr>
<tr><td>31</td><td>32</td><td>33</td></tr>
</table>
</body>
</html>
--------------------------------------------

This is /cgi-bin/ajax.cgi
--------------------------------------------
#!/bin/env python
import random
print "Content-type: text/html;charset=utf-8\r\n"
data =[]
data.append({"one":'Hello world',"two":12345678L,"three":3.1415926})
data.append(['to',"be","or",'not',"to",'be'])
data.append({'title':"that's the question",'random':random.randrange(0,1000000)})
print str(data)
----------------------------------------------
