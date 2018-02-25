import numpy as np

def get_data_set(eval=False):
    if eval:
        file_name = "./data/test.dat"
    else:
        file_name = "./data/train.dat"
    loaded_data = np.fromfile(file_name, dtype=np.uint8)
    reshaped_data = loaded_data.reshape(-1, 192+2)
    images = reshaped_data[:, 2:]
    labels = reshaped_data[:, :2]
    return images, labels
