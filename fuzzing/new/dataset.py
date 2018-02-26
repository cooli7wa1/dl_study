import numpy as np

def get_data_set(eval=False, label_len=2):
    if eval:
        file_name = "./data/test.dat"
    else:
        file_name = "./data/train.dat"
    loaded_data = np.fromfile(file_name, dtype=np.uint8)
    reshaped_data = loaded_data.reshape(-1, 192+label_len)
    images = reshaped_data[:, label_len:]
    labels = reshaped_data[:, :label_len]
    return images, labels

def get_test_separate_data(fuzzing=True, label_len=2):
    if fuzzing:
        file_name = "./data/test_fuzzing.dat"
    else:
        file_name = "./data/test_normal.dat"
    loaded_data = np.fromfile(file_name, dtype=np.uint8)
    reshaped_data = loaded_data.reshape(-1, 192+label_len)
    images = reshaped_data[:, label_len:]
    labels = reshaped_data[:, :label_len]
    return images, labels