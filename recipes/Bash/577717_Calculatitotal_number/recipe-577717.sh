#!/bin/bash
# @date: May 23, 2011
# @author: Shao-Chuan Wang
# Example usage:
# calculate total number of lines of java source files.
# $ line.sh java
# calculate total number of lines of python source files.
# $ line.sh py

line=0
for f in `find . -type f -name "*.$1"`
do
	li=`wc -l $f | awk '{print $1}'`
	let "line = $line + $li"
done
echo "Total lines: $line"
