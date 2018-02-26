import os
import binascii
import random

FUZZING_FOLDER = './fuzzing'
NORMAL_FOLDER = './normal'
OUTPUT_FOLDER = './'
PROPORTION = 2/3  # train_data/total_data
LOG_FILE = OUTPUT_FOLDER + 'gen.log'

log = []

def parse_raw_data_to_bin_list(folder, label):
    files = os.listdir(folder)
    ascii_datas = []
    for fuzzing_file in files:
        with open(os.path.join(folder, fuzzing_file)) as f:
            raw_lines = f.readlines()
            for line in raw_lines:
                line_list = line.replace('\n','').split(" ")
                if len(line_list) == 3 and line_list[2] != '':
                    ascii_datas.append(line_list[2])
    non_repeat_ascii_datas = list(set(ascii_datas))
    log.append("origin data number: %d" % len(ascii_datas))
    log.append("non-repeat data number: %d" % len(non_repeat_ascii_datas))

    bin_list = []
    for ascii_data in non_repeat_ascii_datas:
        ascii_data = label+ascii_data
        bin_data = binascii.unhexlify(ascii_data)
        bin_list.append(bin_data)
    log.append('bin_list len %d' % len(bin_list))
    log.append('bin_list[0] len %d' % len(bin_list[0]))
    return bin_list

def intercept_data(list1, list2):
    num = min(len(list1), len(list2))
    log.append('list1 len %d, list2 len %d, min lne %d' % (len(list1),  len(list2), num))
    intercept_list = list1[:num]
    intercept_list.extend(list2[:num])
    log.append('intercept_list len %d' % len(intercept_list))
    return intercept_list

def shuffle_data(list):
    random.shuffle(list)

def devide_data(list, output_dir):
    total_num = len(list)
    train_num = int(total_num * PROPORTION)
    log.append('total_num %d, train_num %d' % (total_num, train_num))
    with open(output_dir+'train.dat', 'wb') as f:
        for line in list[:train_num]:
            f.write(line)
    with open(output_dir+'test.dat', 'wb') as f:
        for line in list[train_num:]:
            f.write(line)
    log.append('train file size %d' % os.path.getsize(output_dir+'train.dat'))
    log.append('test file size %d' % os.path.getsize(output_dir+'test.dat'))

    test_fuzzing_data = []
    test_normal_data = []
    for line in list[train_num:]:
        if line[:2] == b'\x00\x01':
            test_fuzzing_data.append(line)
        else:
            test_normal_data.append(line)
    with open(output_dir + 'test_fuzzing.dat', 'wb') as f:
        for line in test_fuzzing_data:
            f.write(line)
    with open(output_dir + 'test_normal.dat', 'wb') as f:
        for line in test_normal_data:
            f.write(line)

if __name__ == "__main__":
    # fuzzing_bin_list = parse_raw_data_to_bin_list(FUZZING_FOLDER, '01')
    # log.append("== deal fuzzing .. done")
    # normal_bin_list = parse_raw_data_to_bin_list(NORMAL_FOLDER, '00')
    # log.append("== deal normal .. done")
    fuzzing_bin_list = parse_raw_data_to_bin_list(FUZZING_FOLDER, '0001')
    log.append("== deal fuzzing .. done")
    normal_bin_list = parse_raw_data_to_bin_list(NORMAL_FOLDER, '0100')
    log.append("== deal normal .. done")
    intercept_bin_list = intercept_data(fuzzing_bin_list, normal_bin_list)
    log.append("== intercept .. done")
    shuffle_data(intercept_bin_list)
    log.append("== shuffle .. done")
    devide_data(intercept_bin_list, OUTPUT_FOLDER)
    log.append("== devide .. done")

    with open(LOG_FILE, 'w') as f:
        for line in log:
            f.write(line+'\n')
            print(line)
