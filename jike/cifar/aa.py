import codecs
import struct
import binascii

folder='/home/cooli7wa/PycharmProjects/tensorflow/fuzzing/data/'

f = open(folder+'fuzzing_train_12000', 'r')
f1 = open(folder+'fuzzing_train_12000.dat', 'wb')

for line in f:
    list = [line[i:i+2] for i in range(0, len(line), 2)]
    for str in list:
        if str == '\n':
            continue
        hex = int(str, 16)
        # f1.write(struct.pack('i', hex))
        f1.write(binascii.a2b_uu(chr(hex)))

f.close()
f1.close()

# f1 = open(folder+'fuzzing_train_12000.dat', 'rb')
# print(struct.unpack('i', f1.read()[:4]))
# f1.close()