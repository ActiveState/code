#!/bin/bash

if [ "$#" -eq "0" ]; then
    echo "Args: <INIT> <LOOP> <END>. <LOOP> code can use 'line' variable"
    echo "If -d is given as a first arg, code to be executed is printed"
    exit 1
fi

if [ "$1" = "-d" ]; then
    DEBUG=1
    shift
fi

[ "$#" -eq "1" ] && LOOP="$1"
[ "$#" -eq "2" ] && INIT="$1" && LOOP="$2"
[ "$#" -eq "3" ] && INIT="$1" && LOOP="$2" && END="$3"

CODE="
import sys

$INIT

for line in sys.stdin:
    line = line.strip()
    $LOOP

$END
"

if [ "$DEBUG" = "1" ]; then
    echo $CODE
fi

exec python -c "$CODE"
