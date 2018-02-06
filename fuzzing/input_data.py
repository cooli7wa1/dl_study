import tensorflow as tf
import numpy as np
from config import FLAGS

def _read(filename_queue):
    class FuzzingRecord():
        pass
    result = FuzzingRecord()
    label_bytes = FLAGS.label_size
    data_bytes = FLAGS.data_size
    record_bytes = label_bytes + data_bytes
    reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)
    result.key, value = reader.read(filename_queue)
    record_bytes = tf.decode_raw(value, tf.uint8, little_endian=False)
    result.label = tf.cast(tf.strided_slice(record_bytes, [0],
                                            [label_bytes]), tf.float32)
    result.data = tf.cast(tf.strided_slice(record_bytes, [label_bytes],
                       [label_bytes + data_bytes]), tf.float32)
    result.label = tf.reshape(result.label, [FLAGS.label_size])
    result.data = tf.reshape(result.data, [FLAGS.data_size])
    # result.label.set_shape([1,])
    return result


def input(filenames):
    with tf.name_scope('input'):
        filename_queue = tf.train.string_input_producer(filenames)
        read_input = _read(filename_queue)

        data, label = tf.train.shuffle_batch([read_input.data, read_input.label],
                                             num_threads=16,
                                             batch_size=FLAGS.batch_size,
                                             capacity=FLAGS.capacity,
                                             min_after_dequeue=FLAGS.min_after_dequeue)
    return data, label


def show():
    file_list = [FLAGS.data_dir+FLAGS.train_data]
    data, label = input(file_list)
    with tf.Session() as sess:
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        out_data, out_label = sess.run((data, label))
        print(np.shape(data), np.shape(label))
        for i in range(10):
            print(out_label[i])
        print(out_data[0])
        coord.request_stop()
        coord.join(threads)

if __name__ == '__main__':
    show()
