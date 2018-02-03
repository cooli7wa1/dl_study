import os, re

folder='E:\\PycharmProjects\\dl_study\\fuzzing\\data\\'
ori_files=os.listdir(folder)
target_files=[]
for file in ori_files:
    if re.match(r'^mix_(train|test)[^\.]+$', file):
        target_files.append(file)

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

# f1 = open(folder+'fuzzing_train_12000.dat', 'rb')
# print(struct.unpack('i', f1.read()[:4]))
# f1.close()