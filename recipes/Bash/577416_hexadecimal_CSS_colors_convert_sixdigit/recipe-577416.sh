# shorten your CSS
sed -re 's/#(([0-9a-fA-F])\2)(([0-9a-fA-F])\4)(([0-9a-fA-F])\6)/#\2\4\6/'

# expand: the three-digit RGB notation (#rgb) is converted into six-digit form (#rrggbb) by replicating digits
sed -re 's/#([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])\b/#\1\1\2\2\3\3/'

# works in egrep too
grep -E '(([0-9a-fA-F])\2)(([0-9a-fA-F])\4)(([0-9a-fA-F])\6)'
