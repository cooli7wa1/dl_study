#!/bin/bash

# $1 file1
# $2 file2
# $3 output file_name

function random
{
	min=$1
	max=$(($2-$min+1))
	num=$(cat /dev/urandom | head -n 10 | cksum | awk -F ' ' '{print $1}')
	rand_num=$(($num%$max+$min))
}

if [[ ! -e $1 || ! -e $2 ]];then
	echo "$1 or $2 not exist"
fi

cp $1 $3
line_num1=`cat $1 | wc -l`
line_num2=`cat $2 | wc -l`

jd_step=`expr $((${line_num2}/100))`
jd_i=0
jd_j=0

cat $2 | while read line
do
	random 1 $line_num1
	sed -i "${rand_num}a $line" $3
	((jd_i++))
	if [ `expr $(($jd_i%$jd_step))` -eq 0 ];then
		((jd_j++))
	fi
	printf "progress: %d%%\r" $jd_j
done
echo ""
