import tensorflow as tf
import numpy as np
from config import *

def _read(filename_queue):
    class FuzzingRecord():
        pass
    result = FuzzingRecord()
    label_bytes = 2
    data_bytes = DATA_SIZE*2
    record_bytes = label_bytes + data_bytes
    reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)
    result.key, value = reader.read(filename_queue)
    record_bytes = tf.decode_raw(value, tf.uint8, little_endian=False)
    result.label = tf.cast(tf.strided_slice(record_bytes, [0],
                                            [label_bytes]), tf.int32)
    result.data = tf.cast(tf.strided_slice(record_bytes, [label_bytes],
                       [label_bytes + data_bytes]), tf.float32)
    
    result.data = tf.reshape(result.data, [1,192])
    result.label.set_shape([1])
    return result

def _generate_batch(data, label, min_queue_examples, batch_size):
    pass

def input(filenames, batch_size):
    with tf.name_scope('input'):
        filename_queue = tf.train.string_input_producer(filenames)
        read_input = _read(filename_queue)
        data, label = tf.train.shuffle_batch([read_input.data, read_input.label],
                                             batch_size=10,
                                             capacity=30,
                                             min_after_dequeue=20)
    return data, label

data, label = input(['/home/cooli7wa/study/tensorflow_data/fuzzing_data/clear_data_fuzzing'], 0)
a = tf.Print(data, [data], message='data:')

with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)
    data = sess.run(a)
    print(np.shape(data))
    print(data[0])
    coord.request_stop()
    coord.join(threads)

