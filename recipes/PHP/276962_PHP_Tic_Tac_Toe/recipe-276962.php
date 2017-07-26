<?php

//////////////////////////////////////////////////
//	PHP Tic Tac Toe				//
//	Created : 15/02/03 (dd/mm/yy)		//
// 	(c) 2003 Premshree Pillai		//
//	http://www.qiksearch.com		//
//	http://premshree.resource-locator.com	//
//////////////////////////////////////////////////

global $bsize,$playerToken,$myToken,$gameOver,$winArr,$rowArr,$colArr,$digArr,$vals,$s1,$s2,$s3,$s4,$s5,$s6,$s7,$s8,$s9;

$bsize=3;
$playerToken="X";
$myToken="0";
$gameOver=0;
$winArr=array();

$rowArr=array();
$colArr=array();
$digArr=array();

// Arrays for testing
for($x=0; $x<$bsize*$bsize; $x++)
{
	$rowArr[$x]=0;
	$colArr[$x]=0;
	$digArr[$x]=0;
}
?>
<html>
<head>
<title>Tic Tac Toe in PHP</title>
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
	if(check=="") {
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
<table width="100%" bgcolor="#9999CC" cellspacing="0" cellpadding="0"><tr><td align="center"><a href="tic-tac-toe.php"><img src="ttt_php.gif" border="0" alt="Tic Tac Toe (in PHP)"></a></td></tr></table>
<table width="100%" bgcolor="#EFEFFF" cellspacing="0" cellpadding="0"><tr><td align="center"><a href="http://www.qiksearch.com"><img src="qiksearch_ttt_php.gif" border="0" alt="www.qiksearch.com"></a></td></tr></table>

<?
function genBox($size) {
	global $bsize,$playerToken,$myToken,$gameOver,$winArr,$rowArr,$colArr,$digArr,$vals,$s1,$s2,$s3,$s4,$s5,$s6,$s7,$s8,$s9;

	$count=0;
	$retVal='<form name="ttt" method="post" action="tic-tac-toe.php">';
	for($i=0; $i<$size; $i++) {
		for($j=0; $j<$size; $j++) {
			$count++;
			$retVal.='<input type="button" name="s'.$count.'_btn" value="" class="btn" onClick="toggleVal(\'s'.$count.'\')" onMouseover="this.className=\'btn_over\'" onMouseout="this.className=\'btn\'" onMousedown="this.className=\'btn_down\'"><input type="hidden" name="s'.$count.'" value="">';
		}
		$retVal.='<br>';
	}
	$retVal.='</form>';
	echo $retVal;
}

function genBox2($size,$arr) {
	global $bsize,$playerToken,$myToken,$gameOver,$winArr,$rowArr,$colArr,$digArr,$vals,$s1,$s2,$s3,$s4,$s5,$s6,$s7,$s8,$s9;

	$count=0;
	$retVal='<form name="ttt" method="post" action="tic-tac-toe.php">';
	for($i=0; $i<$size; $i++) {
		for($j=0; $j<$size; $j++) {
			$count++;
			$retVal.='<input type="button" name="s'.$count.'_btn" value="'.$arr[$count-1].'" class="btn" onClick="toggleVal(\'s'.$count.'\')" onMouseover="this.className=\'btn_over\'" onMouseout="this.className=\'btn\'" onMousedown="this.className=\'btn_down\'"><input type="hidden" name="s'.$count.'" value="'.$arr[$count-1].'">';
		}
		$retVal.='<br>';
	}
	$retVal.='</form>';
	echo $retVal;
}

function isEmpty($who) {
	if($who=="")
		return 1;
	else
		return 0;
}

function move($bsize,$arr) {
	global $bsize,$playerToken,$myToken,$gameOver,$winArr,$rowArr,$colArr,$digArr,$vals,$s1,$s2,$s3,$s4,$s5,$s6,$s7,$s8,$s9;

	$count=0;	
	$maxCount=0;
	$pos=0;
	$retVal=0;
	
	# Build Row Array
	for($i=0; $i<$bsize; $i++) {
		$maxCount=0;
		$fullCounter=0;
		for($j=0; $j<$bsize; $j++) {
			$count++;
			$who=$arr[$count-1];
			if($who==$playerToken) {
				$maxCount++;
				$fullCounter++;
			}
			if($who==$myToken)
				$fullCounter++;
		}
		$rowArr[$i]=$maxCount;
		if($fullCounter==$bsize)
			$rowArr[$i]=-1;
	}

	# Building Column Array
	for($i=0; $i<$bsize; $i++) {
		$count=$i+1;
		$maxCount=0;
		$fullCounter=0;
		for($j=0; $j<$bsize; $j++) {
			$who=$arr[$count-1];
			if($who==$playerToken) {
				$maxCount++;
				$fullCounter++;
			}
			if($who==$myToken)
				$fullCounter++;
			$count+=$bsize;
		}
		$colArr[$i]=$maxCount;
		if($fullCounter==$bsize)
			$colArr[$i]=-1;
	}

	# Building Diagonal Array
	for($i=0; $i<2; $i++) {
		if($i==0)
			$count=$i+1;
		else
			$count=$bsize;
		$maxCount=0;
		$fullCounter=0;
		for($j=0; $j<$bsize; $j++) {
			$who=$arr[$count-1];
			if($who==$playerToken) {
				$maxCount++;
				$fullCounter++;
			}
			if($who==$myToken)
				$fullCounter++;
			if($i==0)
				$count+=$bsize+1;
			else
				$count+=$bsize-1;
		}
		$digArr[$i]=$maxCount;
		if($fullCounter==$bsize)
			$digArr[$i]=-1;
	}

	# Finding Max Values
	$maxRow=myMax(0,$bsize,"row",$rowArr);
	$maxCol=myMax(0,$bsize,"col",$colArr);
	$maxDig=myMax(0,$bsize,"dig",$digArr);
	
	$maxArrs[0]=myMax(1,$bsize,"row",$rowArr);
	$maxArrs[1]=myMax(1,$bsize,"col",$colArr);
	$maxArrs[2]=myMax(1,$bsize,"dig",$digArr);
//$maxArrs=array(max(1,$bsize,"row",$rowArr),max(1,$bsize,"col",$colArr),max(1,$bsize,"dig",$digArr));
	if(myMax(0,$bsize,"x",$maxArrs)==0)
		$pos=$bsize*($maxRow+1)-$bsize;
	if(myMax(0,$bsize,"x",$maxArrs)==1)
		$pos=$maxCol;
	if(myMax(0,$bsize,"x",$maxArrs)==2)
		if($maxDig==0)
			$pos=$maxDig;
		else
			$pos=$bsize-1;

	$retFlag=0;
	for($y=0; $y<$bsize; $y++) {
		if(!$retFlag) {
			if($arr[$pos]=="") {
				$retVal=$pos;
				$retFlag=1;
			}
			if(myMax(0,$bsize,"x",$maxArrs)==0)
				$pos++;
			if(myMax(0,$bsize,"x",$maxArrs)==1)
				$pos+=$bsize;
			if(myMax(0,$bsize,"x",$maxArrs)==2)
				if($maxDig==0)
					$pos+=$bsize+1;
				else
					$pos+=$bsize-1;
		}
	}
	return $retVal;
}

function myMax($what,$bsize,$type,$arr) {
	global $bsize,$playerToken,$myToken,$gameOver,$winArr,$rowArr,$colArr,$digArr,$vals,$s1,$s2,$s3,$s4,$s5,$s6,$s7,$s8,$s9;

	$max=-1;
	$maxIndex=-1;
	if($type!="dig") {
		for($i=0; $i<$bsize; $i++) {
			if($arr[$i]>$max) {
				$max=$arr[$i];
				$maxIndex=$i;
			}
		}
	}
	if($type=="dig") {
		for($i=0; $i<2; $i++) {
			if($arr[$i]>$max) {
				$max=$arr[$i];
				$maxIndex=$i;
			}
		}
	}
	if($what==0)
		return $maxIndex;
	else
		return $max;
}

function playerWin() {
	global $bsize,$playerToken,$myToken,$gameOver,$winArr,$rowArr,$colArr,$digArr,$vals,$s1,$s2,$s3,$s4,$s5,$s6,$s7,$s8,$s9;

	$who=$playerToken;
	if(($s1==$who && $s2==$s1 && $s3==$s1) || ($s4==$who && $s5==$s4 && $s6==$s4)||($s7==$who && $s8==$s7 && $s9==$s7) ||($s1==$who && $s4==$s1 && $s7==$s1) ||($s2==$who && $s5==$s2 && $s8==$s2) ||($s3==$who && $s6==$s3 && $s9==$s3) ||($s1==$who && $s5==$s1 && $s9==$s1) ||($s3==$who && $s5==$s3 && $s7==$s3))
		return 1;
	else
		return 0;
}

function iWin() {
	global $bsize,$playerToken,$myToken,$gameOver,$winArr,$rowArr,$colArr,$digArr,$vals,$s1,$s2,$s3,$s4,$s5,$s6,$s7,$s8,$s9;

	$who=$myToken;
	if(($s1==$who && $s2==$s1 && $s3==$s1) || ($s4==$who && $s5==$s4 && $s6==$s4)||($s7==$who && $s8==$s7 && $s9==$s7) ||($s1==$who && $s4==$s1 && $s7==$s1) ||($s2==$who && $s5==$s2 && $s8==$s2) ||($s3==$who && $s6==$s3 && $s9==$s3) ||($s1==$who && $s5==$s1 && $s9==$s1) ||($s3==$who && $s5==$s3 && $s7==$s3))
		return 1;
	else
		return 0;
}

function whereWinComp() {
	global $bsize,$playerToken,$myToken,$gameOver,$winArr,$rowArr,$colArr,$digArr,$vals,$s1,$s2,$s3,$s4,$s5,$s6,$s7,$s8,$s9;

	$who=$myToken;
	if(($s1==$who && $s2==$s1 && $s3==$s1))
		$winArr=array('s1','s2','s3');
	if(($s4==$who && $s5==$s4 && $s6==$s4))
		$winArr=array('s4','s5','s6');
	if(($s7==$who && $s8==$s7 && $s9==$s7))
		$winArr=array('s7','s8','s9');
	if(($s1==$who && $s4==$s1 && $s7==$s1))
		$winArr=array('s1','s4','s7');
	if(($s2==$who && $s5==$s2 && $s8==$s2))
		$winArr=array('s2','s5','s8');
	if(($s3==$who && $s6==$s3 && $s9==$s3))
		$winArr=array('s3','s6','s9');
	if(($s1==$who && $s5==$s1 && $s9==$s1))
		$winArr=array('s1','s5','s9');
	if(($s3==$who && $s5==$s3 && $s7==$s3))
		$winArr=array('s3','s5','s7');
}

function whereWinPlayer() {
	global $bsize,$playerToken,$myToken,$gameOver,$winArr,$rowArr,$colArr,$digArr,$vals,$s1,$s2,$s3,$s4,$s5,$s6,$s7,$s8,$s9;

	$who=$playerToken;
	if(($s1==$who && $s2==$s1 && $s3==$s1))
		$winArr=array('s1','s2','s3');
	if(($s4==$who && $s5==$s4 && $s6==$s4))
		$winArr=array('s4','s5','s6');
	if(($s7==$who && $s8==$s7 && $s9==$s7))
		$winArr=array('s7','s8','s9');
	if(($s1==$who && $s4==$s1 && $s7==$s1))
		$winArr=array('s1','s4','s7');
	if(($s2==$who && $s5==$s2 && $s8==$s2))
		$winArr=array('s2','s5','s8');
	if(($s3==$who && $s6==$s3 && $s9==$s3))
		$winArr=array('s3','s6','s9');
	if(($s1==$who && $s5==$s1 && $s9==$s1))
		$winArr=array('s1','s5','s9');
	if(($s3==$who && $s5==$s3 && $s7==$s3))
		$winArr=array('s3','s5','s7');
}

function draw() {
	global $bsize,$playerToken,$myToken,$gameOver,$winArr,$rowArr,$colArr,$digArr,$vals,$s1,$s2,$s3,$s4,$s5,$s6,$s7,$s8,$s9;

	$drawCounter=0;
	$dCounter=0;
	for($dCounter=0; $dCounter<sizeof($vals); $dCounter++)
		if($vals[$dCounter]!="")
			$drawCounter++;
	if($drawCounter==$bsize*$bsize)
		return 1;
	else
		return 0;
}

if($HTTP_POST_VARS) {
	$s1=$HTTP_POST_VARS["s1"];
	$s2=$HTTP_POST_VARS["s2"];
	$s3=$HTTP_POST_VARS["s3"];
	$s4=$HTTP_POST_VARS["s4"];
	$s5=$HTTP_POST_VARS["s5"];
	$s6=$HTTP_POST_VARS["s6"];
	$s7=$HTTP_POST_VARS["s7"];
	$s8=$HTTP_POST_VARS["s8"];
	$s9=$HTTP_POST_VARS["s9"];
	$vals=array($s1,$s2,$s3,$s4,$s5,$s6,$s7,$s8,$s9);

	if(draw() || playerWin())
		$gameOver=1;

	# Computer's Move!
	$movIndex=move($bsize,$vals);
	if(!$gameOver)
		$vals[$movIndex]=$myToken;

	# Update S's
	if(!$gameOver) {
		if($movIndex==0)
			$s1=$myToken;
		if($movIndex==1)
			$s2=$myToken;
		if($movIndex==2)
			$s3=$myToken;
		if($movIndex==3)
			$s4=$myToken;
		if($movIndex==4)
			$s5=$myToken;
		if($movIndex==5)
			$s6=$myToken;
		if($movIndex==6)
			$s7=$myToken;
		if($movIndex==7)
			$s8=$myToken;
		if($movIndex==8)
			$s9=$myToken;
	}
	genBox2($bsize,$vals);

	if(playerWin()) {
		echo '<font face="verdana,arial,helvetica" color="#009900" size="4"><b>Wow! You Won!</b></font><br><br>';
		echo '<input type="button" onClick="location.href=\'tic-tac-toe.php\'" value="Play Again!" style="background:#CCCCCC; font-weight:bold; cursor:hand"><br><br>';
		whereWinPlayer();
		echo '<script language="JavaScript">';
		for($winCount=0; $winCount<sizeof($winArr); $winCount++)
			echo 'document.ttt.'.$winArr[$winCount].'_btn.style.color=\'#009900\';';
		for($w=0; $w<$bsize*$bsize; $w++)
			if($vals[$w]=="")
				echo 'document.ttt.s'.($w+1).'_btn.disabled=true;';
		echo '</script>';
		$gameOver=1;
	}
	if (iWin() && !$gameOver) {
		echo '<font face="verdana,arial,helvetica" color="#FF0000" size="4"><b>Oops! You Lost!</b></font><br><br>';
		echo '<input type="button" onClick="location.href=\'tic-tac-toe.php\'" value="Play Again!" style="background:#CCCCCC; font-weight:bold; cursor:hand"><br><br>';
		whereWinComp();
		echo '<script language="JavaScript">';
		for($winCount=0; $winCount<sizeof($winArr); $winCount++)
			echo 'document.ttt.'.$winArr[$winCount].'_btn.style.color=\'#FF0000\';';
		for($w=0; $w<$bsize*$bsize; $w++)
			if($vals[$w]=="")
				echo 'document.ttt.s'.($w+1).'_btn.disabled=true;';
		echo '</script>';
		$gameOver=1;
	}
	if(draw() && !playerWin() && !iWin()) {
		echo '<font face="verdana,arial,helvetica" color="#000000" size="4"><b>It\'s a Draw!</b></font><br><br>';
		echo '<input type="button" onClick="location.href=\'tic-tac-toe.php\'" value="Play Again!" style="background:#CCCCCC; font-weight:bold; cursor:hand"><br><br>';
		print '<script language="JavaScript">';
		for($w=0; $w<$bsize*$bsize; $w++)
			if($vals[$w]=="")
				echo 'document.ttt.s'.($w+1).'_btn.disabled=true;';
		echo '</script>';
	}
}
else
	genBox($bsize);
?>

<div style="font-family:verdana,arial,helvetica; font-weight:bold; font-size:10pt; color:#CC0000; background:#EFEFFF; width:100%; padding:3px" id="process"></div>

<table width="100%" bgcolor="#9999CC"><tr><td><span class="footer">&#169; 2004 <a href="http://www.qiksearch.com" class="link">Premshree Pillai</a> | <a href="http://www.guestbookdepot.com/cgi-bin/guestbook.cgi?book_id=374186" class="link">Sign my Guestbook</a>.</span></td></tr></table>
</td></tr></table>
<table width="348" align="center" bgcolor="#9999CC" cellspacing="0" cellpadding="0"><tr><td></td></tr></table>
<table width="346" align="center" bgcolor="#9999CC" cellspacing="0" cellpadding="0"><tr><td></td></tr></table>
</td></tr></table>
</body>
</html>
