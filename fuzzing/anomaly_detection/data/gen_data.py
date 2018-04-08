import os
import binascii
import random

FUZZING_FOLDER = './fuzzing'
NORMAL_FOLDER = './normal'
OUTPUT_FOLDER = './'
POSITIVE_PROP = [0.5,0.3,0.2]  # train/validation/test
NEGATIVE_PROP = [0,0.6,0.4]  # train/validation/test
LOG_FILE = OUTPUT_FOLDER + 'gen.log'

log = []

def hex_string_to_int_string(hex_string):
    l = len(hex_string)
    if l % 2: return None
    int_string = ""
    for i in range(0, l, 2):
        hex_s = '0x' + hex_string[i:i+2]
        int_n = int(hex_s, 16)
        int_string += str(int_n) + " "
    return int_string.rstrip(" ")


def parse_raw_data_to_txt(folder):
    files = os.listdir(folder)
    ascii_datas = []
    for file in files:
        with open(os.path.join(folder, file)) as f:
            raw_lines = f.readlines()
            for line in raw_lines:
                line_list = line.replace('\n','').split(" ")
                if len(line_list) == 3 and line_list[2] != '':
                    ascii_datas.append(line_list[2])
    non_repeat_ascii_datas = list(set(ascii_datas))
    log.append("origin data number: %d" % len(ascii_datas))
    log.append("non-repeat data number: %d" % len(non_repeat_ascii_datas))

    txt_list = []
    for ascii_data in non_repeat_ascii_datas:
        int_string = hex_string_to_int_string(ascii_data)
        txt_list.append(int_string)
    log.append('txt_list len %d' % len(txt_list))
    log.append('txt_list[0] len %d' % len(txt_list[0]))
    return txt_list


def merge_data_to_file(pos_data, neg_data, file_name):
    pos_label = ['1']*len(pos_data)
    neg_label = ['0']*len(neg_data)
    data = pos_data[:]
    data.extend(neg_data)
    label = pos_label[:]
    label.extend(neg_label)
    log.append('deal with %s' % file_name)
    log.append('data total len %d' % len(data))
    log.append('label total len %d' % len(label))
    mix_seq = range(len(data))
    random.shuffle(mix_seq)
    with open(OUTPUT_FOLDER+file_name+'_data.txt', 'w') as f:
        for i in mix_seq:
            f.write(data[i])
            f.write('\n')
    with open(OUTPUT_FOLDER+file_name+'_label.txt', 'w') as f:
        for i in mix_seq:
            f.write(label[i])
            f.write('\n')


def devide_data(list, prop):
    total_num = len(list)
    train_prop, eval_prop, test_prop = prop
    train_num = int(total_num * train_prop)
    eval_num = int(total_num * eval_prop)
    test_num = total_num - train_num - eval_num
    log.append('total_num %d, train_num %d, eval_num %d, test_num %d' %
               (total_num, train_num, eval_num, test_num))
    random.shuffle(list)
    return list[:train_num], list[train_num:train_num+eval_num], list[train_num+eval_num:]


if __name__ == "__main__":
    fuzzing_txt_list = parse_raw_data_to_txt(FUZZING_FOLDER)
    log.append("== deal fuzzing .. done")
    normal_txt_list = parse_raw_data_to_txt(NORMAL_FOLDER)
    log.append("== deal normal .. done")
    pos_train, pos_eval, pos_test = devide_data(fuzzing_txt_list, POSITIVE_PROP)
    log.append("== devide pos .. done")
    neg_train, neg_eval, neg_test = devide_data(normal_txt_list, NEGATIVE_PROP)
    log.append("== devide neg .. done")
    merge_data_to_file(pos_train, neg_train, 'train')
    log.append("== merge train .. done")
    merge_data_to_file(pos_eval, neg_eval, 'eval')
    log.append("== merge eval .. done")
    merge_data_to_file(pos_test, neg_test, 'test')
    log.append("== merge test .. done")

    with open(LOG_FILE, 'w') as f:
        for line in log:
            f.write(line+'\n')
            print(line)
