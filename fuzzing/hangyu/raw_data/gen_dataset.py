#encoding="utf-8"

import sys
import argparse
import re
import json
import binascii

#  np.fromfile("normal.data",dtype=uint8)
def parse_raw_date(input_file, output_file, label = None):
    input_fd = open(input_file, "r")
    raw_list = input_fd.readlines()
    input_fd.close()
    data_list = list()
    if label is not None:
        label_list = list()
    else:
        label_list = None
    #data_regex = re.compile(r'')
    for rd in raw_list:
        data = rd.replace("\n","").split(" ")
        if len(data) != 3 or len(data[2])<1:
            continue
        print("==========")    
        print(data) 
        print(len(data[2]))
        #TODO gen datasets
        fuzzing_block = binascii.unhexlify(data[2])
        print(len(fuzzing_block))
        data_list.append(fuzzing_block)
        if label_list is not None:
            label_list.append(label)
     #save datas
    with open(output_file+".data","wb") as of:
       for i in data_list:
            of.write(i)

    if label_list is not None:
       import struct
       with open(output_file+".label","wb") as of:
           for i in label_list:
               res_array = b'\x00\x01'
               if i == 1:
                   res_array = b'\x01\x00'
               of.write(res_array)
    #save info
    with open(output_file+".info.json","w") as of:
       #of.write("datasets count: %d\n" % len(data_list))
       #of.write("perset size(in byte): %d\n" % len(data_list[0]))
       json.dump({"datasets_count":len(data_list), "perset_size":len(data_list[0])},
                of)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file path.", required=True)
    parser.add_argument("-o", "--output", help="output file prefix.", default="./dataset")
    parser.add_argument("-l", "--label", help="gen label file", default="1")

    args = parser.parse_args()
    print("Reading: %s" % (args.input))
    print("Writing: %s" % (args.output))

    label = None
    if args.label is not None:
        label = int(args.label)

    input_file = args.input
    output_file = args.output

    parse_raw_date(input_file, output_file, label) 
        
