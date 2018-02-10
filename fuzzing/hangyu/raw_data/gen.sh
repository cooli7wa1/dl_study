#!/bin/bash

python gen_dataset.py -i ./fuzzing_data/invokecommand_fuzzing/TZ_fuzzing_invokecommand.txt -o ./fuzzing_invoke -l 1
python gen_dataset.py -i ./fuzzing_data/opensession_fuzzing/TZ_fuzzing_opensession.txt -o ./fuzzing_open -l 1

python gen_dataset.py -i ./session_command_success/opensession_success/TZ_opensession_success.txt -o ./normal_open -l 0
python gen_dataset.py -i ./session_command_success/invokecommand_success/TZ_invokecommand_success.txt -o ./normal_invoke -l 0

cat fuzzing_invoke.data fuzzing_open.data normal_open.data normal_invoke.data > datasets.data
cat fuzzing_invoke.label fuzzing_open.label normal_open.label normal_invoke.label > datasets.label
