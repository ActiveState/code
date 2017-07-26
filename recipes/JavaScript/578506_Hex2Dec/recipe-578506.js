<!DOCTYPE html>
<html>
  <head>
    <title>Hex2Dec</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <script language="javascript" type="text/javascript">
      var num = num || {
        hex2dec : function($) {
          return Number($) ? Number($) : 'Wrong data type';
        },
        
        dec2hex : function($) {
          return Number($) ? '0x' + Number($).toString(16).toUpperCase() : 'Wrong data type';
        },
        
        chkData : function($) {
          if (/^\d+$/g.test($)) return this.dec2hex($);
          else if (/^(0x|x)|^[a-f0-9]+$/ig.test($))
            return !/x/i.test($.slice(0, 1)) ? (/0x/i.test($.slice(0, 2)) ? this.hex2dec($) :
                                                   this.hex2dec('0x' + $)) : this.hex2dec('0' + $);
          else return 'Wrong data type';
        },
        
        onClick : function() {
          document.getElementById('out').value = this.chkData(document.getElementById('in').value);
        }
      };
    </script>
    <style type="text/css">
      body   { font-family: tahoma, sans-serif; }
      h1, h5 { color: #000080; margin-botton: 0; }
      h3     { color: #9933cc; margin-top: 0; padding-top: 0; }
      h1     { font-size: 370%; }
      h5     { font-size: 65%; }
      p      { font-size: 80%; }
    </style>
  </head>
  <body>
<!-- CONTENT BEGIN -->
<center>
  <h1>Hex2Dec</h1>
  <h3>Converts hex to decimal and vice versa</h3>
  <p>Just put something like 250 or 37a into "Input" field and press Enter or click "Convert" to get a result.<br />
  Note that both prefixes '0x' and 'x' are supported. For example, enter 0x200 or x200 to get decimal number.<br />
  Use Esc to clear both "Input" and "Output" fields immediately (if "Input" is in focus).</p>
  <p>Input:&nbsp;&nbsp;&nbsp;<input type="text" id="in" placeholder="hex or dec to get a result"
                                    onkeydown="document.getElementById('in').onkeydown = function($) {
                                                 switch ($.keyCode) {
                                                    case  8:
                                                    case 46:
                                                      document.getElementById('out').value = '';
                                                    break;
                                                    case 13: num.onClick(); break;
                                                    case 27: this.value = document.getElementById('out').value = ''; break;
                                                    default: break;
                                                 }
                                    }"
     />
  </p>
  <p>Output:&nbsp;<input type="text" id="out" /></p>
  <input type="button" value="Convert" onclick="num.onClick();" />
  <h5>Copyright (C) 2010-2013 greg zakharov gregzakh@gmail.com<br />v1.01</h5>
</center>
<!-- END CONTENT -->
  </body>
</html>
