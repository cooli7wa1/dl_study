#!/bin/bash -

input_file_name=$1
data_len=$2
prefix_data=$3
output_file_name=$4

cat $input_file_name | grep -oE "\w{$data_len}" | sed -r "s/.*/$prefix_data&/g" > $output_file_name
