#!/bin/bash

if [[ $# -ne 1 ]];then
    echo "process name?"
    exit 0
fi

all=`ps -A|grep $1`
for i in $all
do
    p=`echo $i |grep -x -o -E "[0-9]+"`
    if [[ -z $p ]]; then
        continue
    fi

    sudo kill $p
done

ps -A|grep $1
