#!/usr/bin/env python3

#encoding = "utf-8"
import numpy as np

class Datasets:
    
    def __init__(self, filename_prefix=None):
        if filename_prefix is None:
            return

        self.data, self.label = self._load_from_file(filename_prefix)   

    def _load_from_file(self, filename_prefix):
        loaded_data = np.fromfile(filename_prefix+".data", dtype = np.uint8)
        loaded_label = np.fromfile(filename_prefix+".label", dtype = np.uint8)
        
        reshaped_data = loaded_data.reshape(-1,192)
        reshaped_label = loaded_label.reshape(-1,2)

        #shuffle and return
        shuffled_index = np.random.permutation(len(reshaped_data))

        return (reshaped_data[shuffled_index], reshaped_label[shuffled_index])

    def get_train_test_sets(self, train_set_rate):
        '''train_rate is a float in [0,1]
        '''
        dataset_count = len(self.data)
        train_index_end = int(dataset_count * train_set_rate)
        return self.data[:train_index_end], self.label[:train_index_end], self.data[train_index_end:], self.label[train_index_end:]
    
    def info(self):
        print("data set count: %d\n" % (len(self.data)))
        print("size per set: %d\n" % (len(self.data[0])))
