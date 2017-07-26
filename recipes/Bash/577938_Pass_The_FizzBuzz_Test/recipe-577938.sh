#!/bin/bash -   
#title          :fizzbuzz.sh
#description    :Pass the fizzbuzz test. Get that job.
#author         :bgw
#date           :20111031
#version        :0.1    
#usage          :./fizzbuzz.sh
#notes          :       
#bash_version   :4.1.5(1)-release
#==============================================================================

for n in {1..100} ; do
    if [ $(expr $n % $((5*3))) -eq 0 ] ; then
        echo FizzBuzz
        sleep 1
    elif [ $(expr $n % 5) -eq 0 ] ; then 
        echo Buzz
        sleep 1
    elif [ $(expr $n % 3) -eq 0 ] ; then 
        echo Fizz
        sleep 1
    else
        echo $n
        sleep 1
    fi
done
