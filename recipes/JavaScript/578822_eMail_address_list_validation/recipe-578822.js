function checkEmail(eadd) {
eadd=eadd.replace(/^[\s]+/, ""); eadd=eadd.replace(/[\s]+$/, "");
if (eadd=="") {alert('Please enter an eMail address'); return false;}
var literal="[\x2D^!#$%&'*+/=?0-9A-Z_`a-z{|}~]+";
var quoted='"[\x20-\x7F]+"';
var word="("+literal+"|"+quoted+")";
var domn="([-0-9A-Z_a-z]+|"+quoted+")";
var emailAdd=word+"([.]"+word+")*@("+domn+"[.])+[a-zA-Z]{2,6}";
var litName="[\x2D\x20^!#$%&'*+/=?0-9A-Z_`a-z{|}~]+";
var quoName='"[\x00-\x09\x0E-\x21\u0023-\uFFFF]+"[\x20\t]*';
var emailFormat="("+emailAdd+"|("+litName+"|"+quoName+")<"+emailAdd+">)";
var emailList=emailFormat+"(,[\x20\t\n]*"+emailFormat+")*";
var emailValid=new RegExp("^"+emailList+"$");
if (emailValid.test(eadd)) return true;
else {
alert('The eMail address you entered has an invalid format. Please check it and try again');
return false; } }
