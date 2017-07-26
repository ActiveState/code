function make_password($length, $lconsonants_on, $uconsonants_on, $lvowels_on, $uvowels_on, $numbers_on, $specials_on){
	$lconsonants	= 'bdghjlmnpqrstvwxz';
	$uconsonants	= 'BDGHJLMNPQRSTVWXZ';
	$lvowels	= 'aeiouy';
	$uvowels	= 'AEIOUY';
	$numbers	= '1234567890';
	$specials	= '@#$%^';
	
	$password	= '';
	
	$select = 1 ;
	
	for ($i = 0; $i < $length; $i++) {
		if ($select == 1) {
			if ($lconsonants_on == 1) {
				$password .= $lconsonants[(rand() % 17)];
			}
			$select = 0;
		}
		else if ($select == 2) {
			if ($uconsonants_on == 1) {
				$password .= $uconsonants[(rand() % 17)];
			}
			$select = 1;
		}
		else if ($select == 3) {
			if ($lvowels_on == 1) {
				$password .= $lvowels[(rand() % 6)];
			}
			$select = 2;
		}
		else if ($select == 4) {
			if ($uvowels_on == 1) {
				$password .= $uvowels[(rand() % 6)];
			}
			$select = 3;
		}
		else if ($select == 5) {
			if ($numbers_on == 1) {
				$password .= $numbers[(rand() % 10)];
			}
			$select = 4;
		}
		else {
			if ($specials_on == 1) {
				$password .= $specials[(rand() % 5)];
			}
			$select = 5;
		}
	}
	return $password;
}


// use this to call the random password

// length = how long the password is
// lconsonants = adds lower case consonants -- 1=on || 0=off
// uconsonants = adds upper case consonants -- 1=on || 0=off
// lvowels = adds lower case vowels -- 1=on || 0=off
// uvowels = adds upper case vowels -- 1=on || 0=off
// numbers = adds numbers -- 1=on || 0=off
// specials = adds @#$%^ -- 1=on || 0=off

// make_password(length, lconsonants, uconsonants, lvowels, uvowels, numbers, specials)
echo make_password(8, 1, 1, 1, 1, 1, 1);
