@set @env=0 /*
  @echo off
    set @env=
    cscript //nologo //e:jscript "%~dpnx0"
  exit /b
*/

var cal = cal || {
  getMonthLastDay : function(year, month) {
    for (var i = 29; i < 33; i++) {
      if (new Date(year, month, i).getMonth() != month) return --i;
    }
  },
  
  setFormatString : function(arr) {
    var str, i;
    for (i = 0; i < arr.length; i++) {
      str = ' ' + arr[i];
      if(str.length == 2) str = ' ' + str;
      WScript.StdOut.Write(str);
    }
    WScript.StdOut.WriteLine();
  },
  
  getCurrentMonth : function() {
    var arr = [], cur, i, mon = {
      0  : '       January',
      1  : '       February',
      2  : '        March',
      3  : '        April',
      4  : '         May',
      5  : '         June',
      6  : '         July',
      7  : '        August',
      8  : '      September',
      9  : '       October',
      10 : '       November',
      11 : '       December'
    };
    with (new Date()) {
      cur = new Date(getYear(), getMonth(), 1).getDay();
      if (cur != 0) {
        for (i = 1; i <= cur; i++) arr.push(' ');
      }
      
      for (i = 1; i <= this.getMonthLastDay(getYear(), getMonth()); i++) {
        arr.push(new Date(getYear(), getMonth(), i).getDate());
      }
      
      WScript.echo(mon[getMonth()]);
      WScript.echo(" Su Mo Tu We Th Fr Sa");
      for (i = 0; i <= arr.length; i += 7) {
        this.setFormatString(arr.slice(i, i + 7));
      }
      WScript.echo("\n Today: " + getDate());
    }
  }
}

WScript.echo(cal.getCurrentMonth());
