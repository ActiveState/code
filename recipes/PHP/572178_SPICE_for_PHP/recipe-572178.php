<!-- START CUSTOM CODE -->

<!-- START TEST FORM -->

<form action="SPICE.php" method="post">
 <p>Your key: <input type="text" name="key" /></p>
 <p>Your text: <input type="text" name="text" /></p>
 <p><input type="submit" /></p>
</form>

<!-- END TEST FORM -->

<!-- START SPICE CODE -->

<?php

################################################################################

# =======
# BLOCK 1
# =======

function crypt_major()
{
	$all = range("\x00", "\xFF");
	shuffle($all);
	$major_key = implode("", $all);
	return $major_key;
}

function crypt_minor()
{
	$sample = array();
	do
	{
		array_push($sample, 0, 1, 2, 3);
	} while (count($sample) != 256);
	shuffle($sample);
	$list = array();
	for ($index = 0; $index < 64; $index++)
	{
		$b12 = $sample[$index * 4] << 6;
		$b34 = $sample[$index * 4 + 1] << 4;
		$b56 = $sample[$index * 4 + 2] << 2;
		$b78 = $sample[$index * 4 + 3];
		array_push($list, $b12 + $b34 + $b56 + $b78);
	}
	$minor_key = implode("", array_map(chr, $list));
	return $minor_key;
}

################################################################################

# =======
# BLOCK 2
# =======

function named_major($name)
{
	srand(crc32($name));
	return crypt_major();
}

function named_minor($name)
{
	srand(crc32($name));
	return crypt_minor();
}

################################################################################

# =======
# BLOCK 3
# =======

function _check_major($key)
{
	if (is_string($key) && strlen($key) == 256)
	{
		foreach (range("\x00", "\xFF") as $char)
		{
			if (substr_count($key, $char) == 0)
			{
				return FALSE;
			}
		}
		return TRUE;
	}
	return FALSE;
}

function _check_minor($key)
{
	if (is_string($key) && strlen($key) == 64)
	{
		$indexs = array();
		foreach (array_map(ord, str_split($key)) as $byte)
		{
			foreach (range(6, 0, 2) as $shift)
			{
				array_push($indexs, ($byte >> $shift) & 3);
			}
		}
		$dict = array_count_values($indexs);
		foreach (range(0, 3) as $index)
		{
			if ($dict[$index] != 64)
			{
				return FALSE;
			}
		}
		return TRUE;
	}
	return FALSE;
}

################################################################################

# =======
# BLOCK 4
# =======

function _encode_map_1($major)
{
	return array_map(ord, str_split($major));
}

function _encode_map_2($minor)
{
	$map_2 = array(array(), array(), array(), array());
	$list = array();
	foreach (array_map(ord, str_split($minor)) as $byte)
	{
		foreach (range(6, 0, 2) as $shift)
		{
			array_push($list, ($byte >> $shift) & 3);
		}
	}
	for ($byte = 0; $byte < 256; $byte++)
	{
		array_push($map_2[$list[$byte]], chr($byte));
	}
	return $map_2;
}

################################################################################

# =======
# BLOCK 5
# =======

function _decode_map_1($minor)
{
	$map_1 = array();
	foreach (array_map(ord, str_split($minor)) as $byte)
	{
		foreach (range(6, 0, 2) as $shift)
		{
			array_push($map_1, ($byte >> $shift) & 3);
		}
	}
	return $map_1;
}

function _decode_map_2($major)
{
	$map_2 = array();
	$temp = array_map(ord, str_split($major));
	for ($byte = 0; $byte < 256; $byte++)
	{
		$map_2[$temp[$byte]] = chr($byte);
	}
	return $map_2;
}

################################################################################

# =======
# BLOCK 6
# =======

function _encode($string, $map_1, $map_2)
{
	$cache = "";
	foreach (str_split($string) as $char)
	{
		$byte = $map_1[ord($char)];
		foreach (range(6, 0, 2) as $shift)
		{
			$cache .= $map_2[($byte >> $shift) & 3][mt_rand(0, 63)];
		}
	}
	return $cache;
}

function _decode($string, $map_1, $map_2)
{
	$cache = "";
	$temp = str_split($string);
	for ($iter = 0; $iter < strlen($string) / 4; $iter++)
	{
		$b12 = $map_1[ord($temp[$iter * 4])] << 6;
		$b34 = $map_1[ord($temp[$iter * 4 + 1])] << 4;
		$b56 = $map_1[ord($temp[$iter * 4 + 2])] << 2;
		$b78 = $map_1[ord($temp[$iter * 4 + 3])];
		$cache .= $map_2[$b12 + $b34 + $b56 + $b78];
	}
	return $cache;
}

################################################################################

# =======
# BLOCK 7
# =======

function encode_string($string, $major, $minor)
{
	if (is_string($string))
	{
		if (_check_major($major) && _check_minor($minor))
		{
			$map_1 = _encode_map_1($major);
			$map_2 = _encode_map_2($minor);
			return _encode($string, $map_1, $map_2);
		}
	}
	return FALSE;
}

function decode_string($string, $major, $minor)
{
	if (is_string($string) && strlen($string) % 4 == 0)
	{
		if (_check_major($major) && _check_minor($minor))
		{
			$map_1 = _decode_map_1($minor);
			$map_2 = _decode_map_2($major);
			return _decode($string, $map_1, $map_2);
		}
	}
	return FALSE;
}

################################################################################

?>

<!-- END SPICE CODE -->

<!-- START TEST CODE -->

<?php

# BLOCK 1 TEST
/*$test11 = crypt_major();
$test12 = crypt_minor();
echo "<br>" . bin2hex($test11) . "<br>";
echo "<br>" . bin2hex($test12) . "<br>";*/

# BLOCK 2 TEST
/*$test21 = named_major($_POST['key']);
$test22 = named_minor($_POST['key']);
echo "<br>" . bin2hex($test21) . "<br>";
echo "<br>" . bin2hex($test22) . "<br>";*/

# BLOCK 3 TEST
/*$test31 = named_major($_POST['key']);
$test32 = named_minor($_POST['key']);
echo "<br>" . _check_major($test31) . "<br>";
echo "<br>" . _check_minor($test32) . "<br>";*/

# BLOCK 4 TEST
/*$test41 = named_major($_POST['key']);
$test42 = named_minor($_POST['key']);
echo "<br>" . print_r(_encode_map_1($test41), TRUE) . "<br>";
echo "<br>" . print_r(_encode_map_2($test42), TRUE) . "<br>";*/

# BLOCK 5 TEST
/*$test51 = named_major($_POST['key']);
$test52 = named_minor($_POST['key']);
echo "<br>" . print_r(_decode_map_1($test52), TRUE) . "<br>";
echo "<br>" . print_r(_decode_map_2($test51), TRUE) . "<br>";*/

# BLOCK 6 & 7 TEST
/*$test671 = named_major($_POST['key']);
$test672 = named_minor($_POST['key']);
echo "<br>" . bin2hex($test671) . "<br>";
echo "<br>" . bin2hex($test672) . "<br>";
if (strlen($_POST['text']) != 0)
{
	$test673 = encode_string($_POST['text'], $test671, $test672);
	$test674 = decode_string($test673, $test671, $test672);
	echo "<br>" . bin2hex($test673) . "<br>";
	echo "<br>" . $test674 . "<br>";
}*/

?>

<!-- END TEST CODE -->

<!-- END CUSTOM CODE -->
