import numpy as np

def get_data_set(eval=False):
    if eval:
        file_name = "/home/cooli7wa/PycharmProjects/tensorflow/fuzzing/hangyu/data/mix_test_6000_test.dat"
    else:
        file_name = "/home/cooli7wa/PycharmProjects/tensorflow/fuzzing/hangyu/data/mix_train_24000_test.dat"
    loaded_data = np.fromfile(file_name, dtype=np.uint8)
    reshaped_data = loaded_data.reshape(-1, 192+2)
    # print(reshaped_data[0])
    images = reshaped_data[:, 2:]
    labels = reshaped_data[:, :2]
    return images, labels
