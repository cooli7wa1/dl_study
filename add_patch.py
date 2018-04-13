import difflib
import argparse
import re

# parser = argparse.ArgumentParser()
# parser.add_argument('-p', '--patch_file', type=str, action='store', required=True)
# parser.add_argument('-t', '--target_file', type=str, action='store', required=True)
# parser.add_argument('-n', '--patch_NUM', type=int, action='store', required=True)
# args = parser.parse_args()
#
# print(args.patch)
# print(args.target)


CHECK_LINES_NUMBER = 3

patch_file = "tmp_patch_1"
target_file = "BoardConfig.mk"
patch_NUM = 10
target_lines = []
patch_lines = []

with open(patch_file, 'r') as f:
    for line in f:
        if re.match(r'^\-\-\- ', line):
            continue
        if re.match(r'^\+\+\+', line):
            continue
        patch_lines.append(line)

def compute_diff(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).ratio()

def find_correct_place(ori_num, ori_str):
    pass

def compute_ori_num(info_num):
    s = re.findall(r'\d+', patch_lines[info_num])
    return int(s[0])+patch_NUM

def make_ori_str(info_num):
    before = []
    after = []
    for i in range(info_num, len(patch_lines)):
        find = False
        if re.match(r'^\+', patch_lines[i]):
            before = patch_lines[info_num+1:i]
            find = True
        if find and re.match(r'^\+', patch_lines[i]):
            after = patch_lines[i]
    pass

for i in range(len(patch_lines)):
    if re.match(r'^@@', patch_lines[i]):
        ori_num = compute_ori_num(i)
        ori_str = make_ori_str(i)
