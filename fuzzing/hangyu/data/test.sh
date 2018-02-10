#!/bin/bash -

cat $1 | while read line
do
	if [[ $line =~ ^00 ]];then
		echo $line
	fi
done
