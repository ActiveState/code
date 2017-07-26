<?php
header('Content-type: text/html');
if (empty($_GET['submit'])) {
	header('Content-type: text/html');
	echo '<form action="?" method="get">';
	echo '<label for="what">Text to hash</label>: ';
	echo '<input type="text" name="what" />';
	echo '<br />';
	echo '<input id="type_all" name="type" type="radio" checked="checked" value="all" />';
	echo '<label for="type_all">all</label>';
	echo '<br />';
	echo '<input id="type_1" name="type" type="radio" value="1" />';
	echo '<label for="type_1">ripemd160</label>';
	echo '<br />';
	echo '<input id="type_2" name="type" type="radio" value="2" />';
	echo '<label for="type_2">SHA256</label>';
	echo '<br />';
	echo '<input id="type_3" name="type" type="radio" value="3" />';
	echo '<label for="type_3">SHA512</label>';
	echo '<br />';
	echo '<input id="type_4" name="type" type="radio" value="4" />';
	echo '<label for="type_4">MD5</label>';
	echo '<br />';
	
	/* To add a new hash type, simply copy the following code and replace
	 * the values enclosed in () by following this list:
	 * ID : the ID you will use to reference the hash type
	 * NAME : the name of the hash you whish to add.

		echo '<input id="type_(ID)" name="type" type="radio" value="(ID)" />';
		echo '<label for="type_(ID)">(NAME)</label>';
		echo '<br />';

	 */
	echo '<input type="submit" value="Submit" name="submit" />';
	echo '<input type="hidden" value="'. time() . '" name="rand" />';
	echo '</form>';
	exit;
}

echo 'Plain text: ' . $_GET['what'] . '<br />';

/* To add a new hash type, first copy the following code and replace 
 * the values enclosed in () by following this list:
 * ID : the same ID used in the other part to reference the hash type
 * NAME :  the name of the hash

	case (ID):
		echo '(NAME): ' . hash("(NAME)", $_GET['what']) . '<br />';
		break;

 * finally, add the following line at the //HERE marker still using the 
 * list displayed earlier.

		echo '(NAME): ' . hash("(NAME)", $_GET['what']) . '<br />';

 */
switch($_GET['type']) {
	case 1:
		echo 'ripemd160: ' . hash("ripemd160", $_GET['what']) . '<br />';
		break;
	case 2:
		echo 'SHA256: ' . hash("sha256", $_GET['what']) . '<br />';
		break;
	case 3:
		echo 'SHA512: ' . hash("sha512", $_GET['what']) . '<br />';
		break;
	case 4:
		echo 'MD5: ' . hash("md5", $_GET['what']) . '<br />';
		break;
	case 'all':
	default:
		echo 'ripemd160: ' . hash("ripemd160", $_GET['what']) . '<br />';
		echo 'SHA256: ' . hash("sha256", $_GET['what']) . '<br />';
		echo 'SHA512: ' . hash("sha512", $_GET['what']) . '<br />';
		echo 'MD5: ' . hash("md5", $_GET['what']) . '<br />';
		//HERE
		break;
}

echo '<br /><a href="' . $_SERVER['PHP_SELF'] . '">Start Again</a>';
?>
