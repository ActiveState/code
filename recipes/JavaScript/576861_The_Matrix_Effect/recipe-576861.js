<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Untitled Document</title>
<style type="text/css">
.matrix { font-family: OCR A Extended; font-size:12pt; text-align:center; width:10px; padding:0px; margin:0px;}
</style>

<script type="text/javascript" language="JavaScript">

<!--
var rows=11; // must be an odd number
var speed=50; // lower is faster
var reveal=2; // between 0 and 2 only. The higher, the faster the word appears
var effectalign="default" //enter "center" to center it.

/***********************************************
* The Matrix Text Effect- by Richard Womersley (http://www.mf2fm.co.uk/rv)
* This notice must stay intact for use
* Visit http://www.dynamicdrive.com/ for full source code
***********************************************/

var w3c=document.getElementById && !window.opera;;
var ie45=document.all && !window.opera;
var ma_tab, matemp, ma_bod, ma_row, x, y, columns, ma_txt, ma_cho;
var m_coch=new Array();
var m_copo=new Array();
window.onload=function() {
	if (!w3c && !ie45) return
  var matrix=(w3c)?document.getElementById("matrix"):document.all["matrix"];
  ma_txt=(w3c)?matrix.firstChild.nodeValue:matrix.innerHTML;
  ma_txt=" "+ma_txt+" ";
  columns=ma_txt.length;
  if (w3c) {
    while (matrix.childNodes.length) matrix.removeChild(matrix.childNodes[0]);
    ma_tab=document.createElement("table");
    ma_tab.setAttribute("border", 0);
    ma_tab.setAttribute("align", effectalign);
    ma_tab.style.backgroundColor="#000000";
    ma_bod=document.createElement("tbody");
    for (x=0; x<rows; x++) {
      ma_row=document.createElement("tr");
      for (y=0; y<columns; y++) {
        matemp=document.createElement("td");
        matemp.setAttribute("id", "Mx"+x+"y"+y);
        matemp.className="matrix";
        matemp.appendChild(document.createTextNode(String.fromCharCode(160)));
        ma_row.appendChild(matemp);
      }
      ma_bod.appendChild(ma_row);
    }
    ma_tab.appendChild(ma_bod);
    matrix.appendChild(ma_tab);
  } else {
    ma_tab='<ta'+'ble align="'+effectalign+'" border="0" style="background-color:#000000">';
    for (var x=0; x<rows; x++) {
      ma_tab+='<t'+'r>';
      for (var y=0; y<columns; y++) {
        ma_tab+='<t'+'d class="matrix" id="Mx'+x+'y'+y+'">&nbsp;</'+'td>';
      }
      ma_tab+='</'+'tr>';
    }
    ma_tab+='</'+'table>';
    matrix.innerHTML=ma_tab;
  }
  ma_cho=ma_txt;
  for (x=0; x<columns; x++) {
    ma_cho+=String.fromCharCode(32+Math.floor(Math.random()*94));
    m_copo[x]=0;
  }
  ma_bod=setInterval("mytricks()", speed);
}

function mytricks() {
  x=0;
  for (y=0; y<columns; y++) {
    x=x+(m_copo[y]==100);
    ma_row=m_copo[y]%100;
    if (ma_row && m_copo[y]<100) {
      if (ma_row<rows+1) {
        if (w3c) {
          matemp=document.getElementById("Mx"+(ma_row-1)+"y"+y);
          matemp.firstChild.nodeValue=m_coch[y];
        }
        else {
          matemp=document.all["Mx"+(ma_row-1)+"y"+y];
          matemp.innerHTML=m_coch[y];
        }
        matemp.style.color="#33ff66";
        matemp.style.fontWeight="bold";
      }
      if (ma_row>1 && ma_row<rows+2) {
        matemp=(w3c)?document.getElementById("Mx"+(ma_row-2)+"y"+y):document.all["Mx"+(ma_row-2)+"y"+y];
        matemp.style.fontWeight="normal";
        matemp.style.color="#00ff00";
      }
      if (ma_row>2) {
          matemp=(w3c)?document.getElementById("Mx"+(ma_row-3)+"y"+y):document.all["Mx"+(ma_row-3)+"y"+y];
        matemp.style.color="#009900";
      }
      if (ma_row<Math.floor(rows/2)+1) m_copo[y]++;
      else if (ma_row==Math.floor(rows/2)+1 && m_coch[y]==ma_txt.charAt(y)) zoomer(y);
      else if (ma_row<rows+2) m_copo[y]++;
      else if (m_copo[y]<100) m_copo[y]=0;
    }
    else if (Math.random()>0.9 && m_copo[y]<100) {
      m_coch[y]=ma_cho.charAt(Math.floor(Math.random()*ma_cho.length));
      m_copo[y]++;
    }
  }
  if (x==columns) clearInterval(ma_bod);
}

function zoomer(ycol) {
  var mtmp, mtem, ytmp;
  if (m_copo[ycol]==Math.floor(rows/2)+1) {
    for (ytmp=0; ytmp<rows; ytmp++) {
      if (w3c) {
        mtmp=document.getElementById("Mx"+ytmp+"y"+ycol);
        mtmp.firstChild.nodeValue=m_coch[ycol];
      }
      else {
        mtmp=document.all["Mx"+ytmp+"y"+ycol];
        mtmp.innerHTML=m_coch[ycol];
      }
      mtmp.style.color="#33ff66";
      mtmp.style.fontWeight="bold";
    }
    if (Math.random()<reveal) {
      mtmp=ma_cho.indexOf(ma_txt.charAt(ycol));
      ma_cho=ma_cho.substring(0, mtmp)+ma_cho.substring(mtmp+1, ma_cho.length);
    }
    if (Math.random()<reveal-1) ma_cho=ma_cho.substring(0, ma_cho.length-1);
    m_copo[ycol]+=199;
    setTimeout("zoomer("+ycol+")", speed);
  }
  else if (m_copo[ycol]>200) {
    if (w3c) {
      mtmp=document.getElementById("Mx"+(m_copo[ycol]-201)+"y"+ycol);
      mtem=document.getElementById("Mx"+(200+rows-m_copo[ycol]--)+"y"+ycol);
    }
    else {
      mtmp=document.all["Mx"+(m_copo[ycol]-201)+"y"+ycol];
      mtem=document.all["Mx"+(200+rows-m_copo[ycol]--)+"y"+ycol];
    }
    mtmp.style.fontWeight="normal";
    mtem.style.fontWeight="normal";
    setTimeout("zoomer("+ycol+")", speed);
  }
  else if (m_copo[ycol]==200) m_copo[ycol]=100+Math.floor(rows/2);
  if (m_copo[ycol]>100 && m_copo[ycol]<200) {
    if (w3c) {
      mtmp=document.getElementById("Mx"+(m_copo[ycol]-101)+"y"+ycol);
      mtmp.firstChild.nodeValue=String.fromCharCode(160);
      mtem=document.getElementById("Mx"+(100+rows-m_copo[ycol]--)+"y"+ycol);
      mtem.firstChild.nodeValue=String.fromCharCode(160);
    }
    else {
      mtmp=document.all["Mx"+(m_copo[ycol]-101)+"y"+ycol];
      mtmp.innerHTML=String.fromCharCode(160);
      mtem=document.all["Mx"+(100+rows-m_copo[ycol]--)+"y"+ycol];
      mtem.innerHTML=String.fromCharCode(160);
    }
    setTimeout("zoomer("+ycol+")", speed);
  }
}
// -->
</script>
</head>

<body>
<div id="matrix">ACTIVE STATE</div>
</body>
</html>
