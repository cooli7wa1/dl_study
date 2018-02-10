import os, re

# folder='E:\\PycharmProjects\\dl_study\\fuzzing\\data\\'
folder='/home/cooli7wa/Documents/dl_study/fuzzing/data/'
ori_files=os.listdir(folder)
target_files=[]
for file in ori_files:
    if re.match(r'^mix_(train|test)[^\.]+$', file):
        target_files.append(file)

# target_files=["mix_train_24000_test"]
target_files=["mix_test_6000_test"]

for file in target_files:
    print('deal with %s ...'%file)
    f = open(folder+file, 'r')
    f1 = open(folder+'%s.dat'%file, 'wb')
    for line in f:
        list = [line[i:i+2] for i in range(0, len(line), 2)]
        for str in list:
            if str == '\n':
                continue
            hex = int(str, 16)
            f1.write(hex.to_bytes(1, byteorder='big'))
    f.close()
    f1.close()
