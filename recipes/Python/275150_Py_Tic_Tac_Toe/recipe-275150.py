#!/usr/bin/env python
#################################################################
##
##	Script:		pyttt.py
##	Author:		Premshree Pillai
##	Description:	Tic-Tac-Toe game in Python
##	Web:		http://www.qiksearch.com/
##			http://premshree.resource-locator.com/
##	Created:	19/03/04 (dd/mm/yy)
##
##	(C) 2004 Premshree Pillai
##
#################################################################

import cgi

print "Content-type: text/html\n\n"

global bsize,playerToken,myToken,gameOver,winArr,rowArr,colArr,digArr,vals,s1,s2,s3,s4,s5,s6,s7,s8,s9

bsize = 3
playerToken = "X"
myToken = "0"
gameOver = 0
winArr = []
rowArr = []
colArr = []
digArr = []

x = 0
while x < bsize * bsize :
	rowArr.append(0)
	colArr.append(0)
	digArr.append(0)
	x = x + 1

out1 = """<html>
<head>
<title>Tic Tac Toe in Python</title>
<style type="text/css">
.main{border:#9999CC solid 2px; width:350px}
.btn{font-family:comic sans ms,verdana,arial,helvetica; font-size:20pt; font-weight:bold; background:#9999CC; width:50px; height:50px; border:#666699 solid 1px; cursor:hand; color:#EFEFFF}
.btn_over{font-family:comic sans ms,verdana,arial,helvetica; font-size:20pt; font-weight:bold; background:#EFEFFF; width:50px; height:50px; border:#666699 solid 1px; cursor:hand; color:#9999CC}
.btn_down{font-family:comic sans ms,verdana,arial,helvetica; font-size:20pt; font-weight:bold; background:#666699; width:50px; height:50px; border:#666699 solid 1px; cursor:hand; color:#EFEFFF}
.footer{font-family:verdana,arial,helvetica; font-size:8pt; color:#FFFFFF}
.link{font-family:verdana,arial,helvetica; font-size:8pt; color:#FFFFFF}
.link:hover{font-family:verdana,arial,helvetica; font-size:8pt; color:#EFEFFF}
</style>
<script language="JavaScript">
var doneFlag=false;
function toggleVal(who) {
	var check;
	eval('check=document.ttt.'+who+'_btn.value;');
	if(check==" ") {
		if(!doneFlag) {
			eval('document.ttt.'+who+'_btn.value="X";');
			eval('document.ttt.'+who+'_btn.disabled="true";');
			eval('document.ttt.'+who+'.value="X";');
			document.ttt.submit();
			doneFlag=true;
			document.getElementById('process').innerHTML="Processing.........";
		}
	}
	else {
		alert('Invalid Move!');
	}
}
</script>
</head>
<body>
<table width="100%" height="100%"><tr><td align="center">
<table width="346" align="center" bgcolor="#9999CC" cellspacing="0" cellpadding="0"><tr><td></td></tr></table>
<table width="348" align="center" bgcolor="#9999CC" cellspacing="0" cellpadding="0"><tr><td></td></tr></table>
<table align="center" cellspacing="0" cellpadding="0" class="main"><tr><td align="center">
<table width="100%" bgcolor="#9999CC" cellspacing="0" cellpadding="0"><tr><td align="center"><a href="pyttt.py"><img src="../ttt_py.gif" border="0" alt="Tic Tac Toe (in Python)"></a></td></tr></table>
<table width="100%" bgcolor="#EFEFFF" cellspacing="0" cellpadding="0"><tr><td align="center"><a href="http://www.qiksearch.com"><img src="../qiksearch_ttt_py.gif" border="0" alt="www.qiksearch.com"></a></td></tr></table>"""

print out1

def genBox(size):
	global bsize,playerToken,myToken,gameOver,winArr,rowArr,colArr,digArr,vals,s1,s2,s3,s4,s5,s6,s7,s8,s9
	count = 0
	retVal = '<form name="ttt" method="post" action="pyttt.py">'
	i = 0
	while i < size :
		j = 0
		while j < size :
			count = count + 1
			retVal = retVal + '<input type="button" name="s' + str(count) + '_btn" value=" " class="btn" onClick="toggleVal(\'s' + str(count) + '\')" onMouseover="this.className=\'btn_over\'" onMouseout="this.className=\'btn\'" onMousedown="this.className=\'btn_down\'"><input type="hidden" name="s' + str(count) + '" value=" ">'
			j = j + 1
		retVal = retVal + '<br>'
		i = i + 1
	retVal = retVal + '</form>'
	print retVal

def genBox2(size,arr):
	global bsize,playerToken,myToken,gameOver,winArr,rowArr,colArr,digArr,vals,s1,s2,s3,s4,s5,s6,s7,s8,s9
	count = 0
	retVal = '<form name="ttt" method="post" action="pyttt.py">'
	i = 0
	while i < size :
		j = 0
		while j < size :
			count = count + 1
			retVal = retVal + '<input type="button" name="s' + str(count) + '_btn" value="' + str(arr[count-1]) + '" class="btn" onClick="toggleVal(\'s' + str(count) + '\')" onMouseover="this.className=\'btn_over\'" onMouseout="this.className=\'btn\'" onMousedown="this.className=\'btn_down\'"><input type="hidden" name="s' + str(count) + '" value="' + str(arr[count-1]) + '">'
			j = j + 1
		retVal = retVal + '<br>'
		i = i + 1
	retVal = retVal + '</form>'
	print retVal

def isEmpty(who):
	if who == " ":
		return 1
	else:
		return 0;


def move(bsize,arr):
	global playerToken,myToken,gameOver,winArr,rowArr,colArr,digArr,vals,s1,s2,s3,s4,s5,s6,s7,s8,s9

	count = 0
	maxCount = 0
	pos = 0
	retVal = 0
	
	# Build Row Array
	i = 0
	while i < bsize :
		maxCount = 0
		fullCounter = 0
		j = 0
		while j < bsize :
			count = count + 1
			who = arr[count-1]
			if who == playerToken :
				maxCount = maxCount + 1
				fullCounter = fullCounter + 1
			if who == myToken :
				fullCounter = fullCounter + 1
			j = j + 1
		rowArr[i] = maxCount
		if fullCounter == bsize :
			rowArr[i] = -1
		i = i + 1

	# Building Column Array
	i = 0
	while i < bsize :
		count = i + 1
		maxCount = 0
		fullCounter = 0
		j = 0
		while j < bsize :
			who = arr[count-1]
			if who == playerToken :
				maxCount = maxCount + 1
				fullCounter = fullCounter + 1
			if who == myToken :
				fullCounter = fullCounter + 1
			count = count + bsize
			j = j + 1
		colArr[i] = maxCount
		if fullCounter == bsize :
			colArr[i] = -1
		i = i + 1

	# Building Diagonal Array
	i = 0
	while i < 2 :
		if i  == 0 :
			count = i + 1
		else:
			count = bsize
		maxCount = 0
		fullCounter = 0
		j = 0
		while j < bsize :
			who = arr[count-1]
			if who == playerToken :
				maxCount = maxCount + 1
				fullCounter = fullCounter + 1
			if who == myToken :
				fullCounter = fullCounter + 1
			if i == 0 :
				count = count + bsize + 1
			else:
				count = count + bsize - 1
			j = j + 1
		digArr[i] = maxCount
		if fullCounter == bsize :
			digArr[i] = -1
		i = i + 1

	# Finding Max Values
	maxRow = myMax(0,bsize,"row",rowArr)
	maxCol = myMax(0,bsize,"col",colArr)
	maxDig = myMax(0,bsize,"dig",digArr)
	
	maxArrs = []
	maxArrs.append(myMax(1,bsize,"row",rowArr))
	maxArrs.append(myMax(1,bsize,"col",colArr))
	maxArrs.append(myMax(1,bsize,"dig",digArr))

	if myMax(0,bsize,"x",maxArrs) == 0 :
		pos = bsize * (maxRow + 1) - bsize
	if myMax(0,bsize,"x",maxArrs) == 1 :
		pos = maxCol
	if myMax(0,bsize,"x",maxArrs) == 2 :
		if maxDig == 0 :
			pos = maxDig
		else:
			pos = bsize - 1

	retFlag = 0
	y = 0
	while y < bsize :
		if not(retFlag):
			if arr[pos] == " " :
				retVal = pos
				retFlag = 1
			if myMax(0,bsize,"x",maxArrs) == 0 :
				pos = pos + 1
			if myMax(0,bsize,"x",maxArrs) == 1 :
				pos = pos + bsize
			if myMax(0,bsize,"x",maxArrs) == 2 :
				if maxDig == 0 :
					pos = pos + bsize + 1
				else:
					pos = pos + bsize - 1
		y = y + 1
	return retVal

def myMax(what,bsize,type,arr):
	global playerToken,myToken,gameOver,winArr,rowArr,colArr,digArr,vals,s1,s2,s3,s4,s5,s6,s7,s8,s9

	max = -1
	maxIndex = -1
	if type != "dig" :
		i = 0
		while i < bsize :
			if arr[i] > max :
				max = arr[i]
				maxIndex = i
			i = i + 1
	if type == "dig" :
		i = 0
		while i < 2 :
			if arr[i] > max :
				max = arr[i]
				maxIndex = i
			i = i + 1
	if what == 0 :
		return maxIndex
	else:
		return max

def playerWin():
	global bsize,playerToken,myToken,gameOver,winArr,rowArr,colArr,digArr,vals,s1,s2,s3,s4,s5,s6,s7,s8,s9

	who = playerToken
	if (s1 == who == s2 == s3) or (s4 == who == s5 == s6) or (s7 == who == s8 == s9) or (s1 == who == s4 == s7) or (s2 == who == s5 == s8) or (s3 == who == s6 == s9) or (s1 == who == s5 == s9) or (s3 == who == s5 == s7) :
		return 1
	else:
		return 0

def iWin():
	global bsize,playerToken,myToken,gameOver,winArr,rowArr,colArr,digArr,vals,s1,s2,s3,s4,s5,s6,s7,s8,s9

	who = myToken
	if (s1 == who == s2 == s3) or (s4 == who == s5 == s6) or (s7 == who == s8 == s9) or (s1 == who == s4 == s7) or (s2 == who == s5 == s8) or (s3 == who == s6 == s9) or (s1 == who == s5 == s9) or (s3 == who == s5 == s7) :
		return 1
	else:
		return 0

def whereWinComp():
	global bsize,playerToken,myToken,gameOver,winArr,rowArr,colArr,digArr,vals,s1,s2,s3,s4,s5,s6,s7,s8,s9

	who = myToken
	if (s1 == who == s2 == s3) :
		winArr = ['s1','s2','s3']
	if (s4 == who == s5 == s6) :
		winArr = ['s4','s5','s6']
	if (s7 == who == s8 == s9) :
		winArr = ['s7','s8','s9']
	if (s1 == who == s4 == s7) :
		winArr = ['s1','s4','s7']
	if (s2 == who == s5 == s8) :
		winArr = ['s2','s5','s8']
	if (s3 == who == s6 == s9) :
		winArr = ['s3','s6','s9']
	if (s1 == who == s5 == s9) :
		winArr = ['s1','s5','s9']
	if (s3 == who == s5 == s7) :
		winArr = ['s3','s5','s7']

def whereWinPlayer():
	global bsize,playerToken,myToken,gameOver,winArr,rowArr,colArr,digArr,vals,s1,s2,s3,s4,s5,s6,s7,s8,s9

	who = playerToken
	if (s1 == who == s2 == s3) :
		winArr = ['s1','s2','s3']
	if (s4 == who == s5 == s6) :
		winArr = ['s4','s5','s6']
	if (s7 == who == s8 == s9) :
		winArr = ['s7','s8','s9']
	if (s1 == who == s4 == s7) :
		winArr = ['s1','s4','s7']
	if (s2 == who == s5 == s8) :
		winArr = ['s2','s5','s8']
	if (s3 == who == s6 == s9) :
		winArr = ['s3','s6','s9']
	if (s1 == who == s5 == s9) :
		winArr = ['s1','s5','s9']
	if (s3 == who == s5 == s7) :
		winArr = ['s3','s5','s7']

def draw():
	global bsize,playerToken,myToken,gameOver,winArr,rowArr,colArr,digArr,vals,s1,s2,s3,s4,s5,s6,s7,s8,s9

	drawCounter = 0
	dCounter = 0
	while dCounter < len(vals) :
		if vals[dCounter] != " " :
			drawCounter = drawCounter + 1
		dCounter = dCounter + 1
	if drawCounter == bsize * bsize :
		return 1
	else:
		return 0

form = cgi.FieldStorage()
if form :
	s1 = form['s1'].value
	s2 = form['s2'].value
	s3 = form['s3'].value
	s4 = form['s4'].value
	s5 = form['s5'].value
	s6 = form['s6'].value
	s7 = form['s7'].value
	s8 = form['s8'].value
	s9 = form['s9'].value
	vals = [s1,s2,s3,s4,s5,s6,s7,s8,s9]

	if draw() or playerWin() :
		gameOver = 1

	# Computer's Move!
	movIndex = move(bsize,vals)
	if not(gameOver) :
		vals[movIndex] = myToken

	# Update S's
	if not(gameOver) :
		if movIndex == 0 :
			s1 = myToken
		if movIndex == 1 :
			s2 = myToken
		if movIndex == 2 :
			s3 = myToken
		if movIndex == 3 :
			s4 = myToken
		if movIndex == 4 :
			s5 = myToken
		if movIndex == 5 :
			s6 = myToken
		if movIndex == 6 :
			s7 = myToken
		if movIndex == 7 :
			s8 = myToken
		if movIndex == 8 :
			s9 = myToken
	genBox2(bsize,vals)

	if playerWin() :
		print '<font face="verdana,arial,helvetica" color="#009900" size="4"><b>Wow! You Won!</b></font><br><br>'
		print '<input type="button" onClick="location.href=\'pyttt.py\'" value="Play Again!" style="background:#CCCCCC; font-weight:bold; cursor:hand"><br><br>'
		whereWinPlayer()
		print '<script language="JavaScript">'
		winCount = 0
		while winCount < len(winArr) :
			print 'document.ttt.' + winArr[winCount] + '_btn.style.color=\'#009900\';'
			winCount = winCount + 1
		w = 0
		while w < (bsize * bsize) :
			if vals[w] == " " :
				print 'document.ttt.s' + str(w + 1) + '_btn.disabled=true;'
			w = w + 1
		print '</script>'
		gameOver = 1

	if iWin() and not(gameOver) :
		print '<font face="verdana,arial,helvetica" color="#FF0000" size="4"><b>Oops! You Lost!</b></font><br><br>'
		print '<input type="button" onClick="location.href=\'pyttt.py\'" value="Play Again!" style="background:#CCCCCC; font-weight:bold; cursor:hand"><br><br>'
		whereWinComp()
		print '<script language="JavaScript">'
		winCount = 0
		while winCount < len(winArr) :
			print 'document.ttt.' + winArr[winCount] + '_btn.style.color=\'#FF0000\';';
			winCount = winCount + 1
		w = 0
		while w < bsize * bsize :
			if vals[w] == " " :
				print 'document.ttt.s' + str(w + 1) + '_btn.disabled=true;'
			w = w + 1
		print '</script>'
		gameOver = 1

	if draw() and not(playerWin()) and not(iWin()) :
		print '<font face="verdana,arial,helvetica" color="#000000" size="4"><b>It\'s a Draw!</b></font><br><br>'
		print '<input type="button" onClick="location.href=\'pyttt.py\'" value="Play Again!" style="background:#CCCCCC; font-weight:bold; cursor:hand"><br><br>'
		print '<script language="JavaScript">'
		w = 0
		while w < bsize * bsize :
			if vals[w] == " " :
				print 'document.ttt.s' + str(w + 1) + '_btn.disabled=true;'
			w = w + 1
		print '</script>'
else:
	genBox(bsize)

out2 = """<div style="font-family:verdana,arial,helvetica; font-weight:bold; font-size:10pt; color:#CC0000; background:#EFEFFF; width:100%; padding:3px" id="process"></div>

<table width="100%" bgcolor="#9999CC"><tr><td><span class="footer">&#169; 2004 <a href="http://www.qiksearch.com" class="link">Premshree Pillai</a> | <a href="http://www.guestbookdepot.com/cgi-bin/guestbook.cgi?book_id=374186" class="link">Sign my Guestbook</a>.</span></td></tr></table>
</td></tr></table>
<table width="348" align="center" bgcolor="#9999CC" cellspacing="0" cellpadding="0"><tr><td></td></tr></table>
<table width="346" align="center" bgcolor="#9999CC" cellspacing="0" cellpadding="0"><tr><td></td></tr></table>
</td></tr></table>
</body>
</html>"""

print out2
