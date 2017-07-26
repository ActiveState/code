#!/bin/bash

if [ -z "$1" ]; then loc=$(pwd); else loc=$1; fi
ls -R $loc | grep ':$' | sed -e 's/:$//;s/[^-][^\/]*\//--/g;s/^/ /;s/-/|/'
