#!/bin/bash

num="\033[1;36m"
end="\033[0m"

read -p "Enter your mail: " name
read -p "Enter pass of mail: " pass

atom=`wget -qO - https://$name:$pass@mail.google.com/mail/feed/atom \
  --secure-protocol=TLSv1 -T 3 -t 1 --no-check-certificate | grep \
  fullcount | sed -e 's/<fullcount>\(.*\)<\/fullcount>/\1/'`

echo -e 'You have '$num$atom$end' new letters.'
