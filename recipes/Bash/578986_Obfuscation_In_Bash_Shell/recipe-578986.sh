#/bin/bash
# (strings.sh)
# obfuscate.sh
# OSX 10.7.5, default bash terminal.
for n in a b c d e f g h i j k l m n o p q r s t u v w x y z
do
	eval A$n="$n"
done
for n in A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
do
	eval A$n="$n"
done
num=0
for n in a b c d e f g h i j
do
	eval B$n="$num"
	num=$((num+1))
done
Bk=' ';Bl='!';Bm='"';Bn='#';Bo='$';Bp='%';Bq='&';Br="'"
Bs='(';Bt=')';Bu='*';Bv='+';Bw=',';Bx='-';By='.';Bz='/'
Ca=':';Cb=';';Cc='<';Cd='=';Ce='>';Cf='?';Cg='@';Ch='['
Ci='\';Cj=']';Ck='^';Cl='_';Cm='`';Cn='{';Co='|';Cp='}'
Cq='~'
# A program using $string format only...
#
# clear
$Ac$Al$Ae$Aa$Ar
# eval name=""
$Ae$Av$Aa$Al$Bk$An$Aa$Am$Ae$Cd$Bm$Bm
# eval age=""
$Ae$Av$Aa$Al$Bk$Aa$Ag$Ae$Cd$Bm$Bm
# eval printf "Enter your full name:-\n"
$Ae$Av$Aa$Al$Bk$Ap$Ar$Ai$An$At$Af$Bk$Bm$AE$An$At$Ae$Ar$Bk$Ay$Ao$Au$Ar$Bk$Af$Au$Al$Al$Bk$An$Aa$Am$Ae$Ca$Bx$Ci$An$Bm
# read name
$Ar$Ae$Aa$Ad$Bk$An$Aa$Am$Ae
# eval printf "Enter your age:-\n"
$Ae$Av$Aa$Al$Bk$Ap$Ar$Ai$An$At$Af$Bk$Bm$AE$An$At$Ae$Ar$Bk$Ay$Ao$Au$Ar$Bk$Aa$Ag$Ae$Ca$Bx$Ci$An$Bm
# read age
$Ar$Ae$Aa$Ad$Bk$Aa$Ag$Ae
# eval printf "Hi Barry Walker, you are 63 years old.\n"
$Ae$Av$Aa$Al$Bk$Ap$Ar$Ai$An$At$Af$Bk$Bm$AH$Ai$Bk$name$Bw$Bk$Ay$Ao$Au$Bk$Aa$Ar$Ae$Bk$age$Bk$Ay$Ae$Aa$Ar$As$Bk$Ao$Al$Ad$By$Ci$An$Bm
