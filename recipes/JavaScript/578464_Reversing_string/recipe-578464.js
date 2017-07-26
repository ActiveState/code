//with cycle (not recommended)
function StrReverse(str) {
  var res = '';
  for (var i = str.length - 1; i >= 0; --i)
    res += str.charAt(i);

  return(res);
}

alert(StrReverse(".gnirts a si sihT"));

//creating prototype
String.prototype.reverse = function() {
  return this.split('').reverse().join('');
}

alert(new String(".gnirts a si sihT").reverse());
