import difflib
import argparse
import re

RETURN_FILE = './tmp_return.txt'

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--patch_file', type=str, action='store', required=True)
parser.add_argument('-t', '--target_file', type=str, action='store', required=True)
parser.add_argument('-n', '--check_number', type=int, action='store', required=True)
args = parser.parse_args()

target_file = args.target_file
patch_file = args.patch_file
check_number = args.check_number

# target_file = "tmp_target_Makefile"
# patch_file = "tmp_patch_Makefile"
# check_number = 3

with open(patch_file, 'r') as f:
    patch_lines = f.readlines()
with open(target_file, 'r') as f:
    target_lines = f.readlines()

def strip_str(str):
    str = re.sub('[ \t]+','',str)
    str = re.sub('\n','',str)
    return str

def compute_diff(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).ratio()

def find_correct_place(block_str, crawl):
    """
    :param block_str: strip string
    :param crawl: [pre_len, post_len]
    :return: [place, prop, str]
            place: insert line number in target file
            prop: match probability
            str: strip string
    """
    max_prop, place, max_str = 0, 0, ""
    i = 0
    while i <= len(target_lines)-sum(crawl):
        n, j, str, p = 0, i, "", 0
        while j <= len(target_lines)-1 and n < sum(crawl):
            if target_lines[j].strip() is not '':
                str += target_lines[j]
                n += 1
            if n == crawl[0]:
                p = j
            j += 1
        str = strip_str(str)
        prop = compute_diff(str, block_str)
        if prop > max_prop:
            max_prop, place, max_str = prop, p, str
            if prop == 1:
                break
        i += 1
    return [place+1, max_prop, max_str]

def split_blocks(info_num_in_patch):
    """
    :param info_num_in_patch: "@@.." info's line number in patch file
    :return: blocks in this info, each block is a list, [[start,end],[start_in_origin, end_in_origin], [pre,post]]
            start: block start line in patch file
            end: block end line in patch file
            start_in_origin: block start line in origin file
            end_in_origin: block end line in origin file
            pre: block pre lines'number, often is CHECK_LINES_NUMBER
            post: block post lines'number, often is  CHECK_LINES_NUMBER
    """
    blocks = []
    start_number_in_origin = int(re.findall(r'\d+', patch_lines[info_num_in_patch])[0])
    start_in_patch, end_in_patch, interval = 0, 0, 0
    find = False
    for i in range(info_num_in_patch+1, len(patch_lines)):
        if re.match(r'^@@', patch_lines[i]):
            break
        if not find:
            if re.match(r'^\+', patch_lines[i]):
                start_in_patch = i
                find = True
            else:
                if patch_lines[i].strip != '':
                    interval += 1
        if find and not (re.match(r'^\+', patch_lines[i]) or patch_lines[i].strip() == ''):
            if patch_lines[i - 1].strip() == '':
                end_in_patch = i - 2
            else:
                end_in_patch = i - 1
            start = start_in_patch - info_num_in_patch - 1 + start_number_in_origin
            end = end_in_patch - info_num_in_patch - 1 + start_number_in_origin
            blocks.append([[start_in_patch,end_in_patch],[start,end],[interval]])
            find, interval = False, 1
    n = len(blocks)
    for i in range(n):
        blocks[i][2][0] = min(blocks[i][2][0], check_number)
        if i == n-1:
            blocks[i][2].append(check_number)
        else:
            blocks[i][2].append(min(blocks[i+1][2][0], check_number))
    return blocks

def make_block_str(block):
    start, end, pre, post = block[0][0], block[0][1], block[2][0], block[2][1]
    before, after = "", ""
    n = 0
    for j in range(start-1, -1, -1):
        if patch_lines[j].strip() is not '':
            before = patch_lines[j] + before
            n += 1
            if n >= pre:
                break
    n = 0
    for j in range(end+1, len(patch_lines)):
        if patch_lines[j].strip() is not '':
            after += patch_lines[j]
            n += 1
            if n >= post:
                break
    return strip_str(before + after)

f = open(RETURN_FILE, 'w')
place_row_offset = 0
origin_row_offset = 0
for i in range(len(patch_lines)):
    if re.match(r'^@@', patch_lines[i]):
        origin_offset = 0
        blocks = split_blocks(i)
        # print(blocks)
        for block in blocks:
            # print(block)
            block_str = make_block_str(block)
            # print(block_str)
            [place, prop, str] = find_correct_place(block_str, block[2])
            # print(str)
            # print(place, prop)
            origin_start_line = block[1][0] + origin_row_offset
            origin_end_line = block[1][1] + origin_row_offset
            target_insert_line = place + place_row_offset
            f.write("%d %d %d %.02f\n" % (origin_start_line, origin_end_line, target_insert_line, prop))
            place_row_offset += block[1][1] - block[1][0] + 1
            origin_offset += block[1][1] - block[1][0] + 1
        origin_row_offset += origin_offset
f.close()

