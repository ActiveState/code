epy () {
	cmd="import $1 as a ; print a.__file__.endswith('.pyc') and a.__file__[:-1] or a.__file__" 
	file=$(/usr/bin/env python -c $cmd) 
	echo $file
	emacsclient --no-wait $file
}
