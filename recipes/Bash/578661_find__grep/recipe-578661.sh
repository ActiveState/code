#!/usr/bin/env zsh

tmp_file="$(mktemp)"
echo "--- find <$2> in <$1>" > $tmp_file

find . -follow -iname "$1" | while read file
do
	timestamp=$(ls -l --time-style=+"%Y-%m-%d %H:%M:%S" "$file" | gawk '{print $6, $7}')
	linestack=${(@f)$(egrep "$2" "$file")}
	for line in $linestack 
	do
		echo "$timestamp $file: $line" >> $tmp_file
	done
done

cat $tmp_file | sort
rm $tmp_file
