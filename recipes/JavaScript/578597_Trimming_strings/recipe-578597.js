//anonymous function
(function() {
  this.trim  = function($) { return $.replace(/^\s+|\s+$/g, ''); };
  this.lTrim = function($) { return $.replace(/^\s+/, ''); };
  this.rTrim = function($) { return $.replace(/\s+$/, ''); };
})();

/*
alert("\"" + trim(" test string ") + "\"");
alert("\"" + lTrim(" test string ") + "\"");
alert("\"" + rTrim(" test string ") + "\"");
*/

//prototypes
String.prototype.trim  = function() {
  return this.replace(/^\s+|\s+$/g, '');
}
String.prototype.lTrim = function() {
  return this.replace(/^\s+/, '');
}
String.prototype.rTrim = function() {
  return this.replace(/\s+$/, '');
}

/*
alert("\"" + " test string ".trim() + "\"");
alert("\"" + " test string ".lTrim() + "\"");
alert("\"" + " test string ".rTrim() + "\"");
*/
