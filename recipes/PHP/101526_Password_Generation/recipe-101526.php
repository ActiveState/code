<?php

function make_password($length){
    $vowels = 'aeiouy';
    $consonants = 'bdghjlmnpqrstvwxz';
    $password = '';
    
    $alt = time() % 2;
    srand(time());

    for ($i = 0; $i < $length; $i++) {
        if ($alt == 1) {
            $password .= $consonants[(rand() % 17)];
            $alt = 0;
        } else {
            $password .= $vowels[(rand() % 6)];
            $alt = 1;
        }
    }
    return $password;
}

echo make_password(8);
?>
