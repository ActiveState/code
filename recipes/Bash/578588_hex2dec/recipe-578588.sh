#!/bin/bash

err="\033[1;31m"
res="\033[1;36m"
end="\033[0m"

if [ $# -eq 1 ]; then
   n=$1
   case $n in
      *[[:xdigit:]])
         if [[ ${n:0:2} =~ 0[xX] ]]; then
            echo -e $res$n' = '$(($n))$end
         elif [[ ${n:0:1} =~ [xX] ]]; then
            echo -e $res'0'$n' = '$((0$n))$end
         elif [[ ${n:0:1} =~ [[:digit:]] && ! $n =~ [[:alpha:]] ]]; then
            printf $res$n' = 0x%X\n'$end $n
         elif [[ ${n:0:1} =~ [[:xdigit:]] ]]; then
            echo -e $res'0x'$n' = '$((0x$n))$end
         else
            echo -e $err'=>err'$end
         fi;;
      *)
         echo -e $err'=>err'$end;;
   esac
else
   echo -e $err'=>err'$end
fi
