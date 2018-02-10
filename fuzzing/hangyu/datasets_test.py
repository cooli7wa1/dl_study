
# coding: utf-8

# import anit_fuzzing_dataset
# dataset = anit_fuzzing_dataset.Datasets("./raw_data/datasets")
# train_X, train_y, test_X, test_y = dataset.get_train_test_sets(0.8)
# print(train_X.shape, train_y.shape)
# print(test_X.shape, test_y.shape)

from read_dataset_mine import get_data_set
train_X, train_y = get_data_set(False)
test_X, test_y = get_data_set(True)
print(train_X.shape, train_y.shape)
print(test_X.shape, test_y.shape)

import tensorflow as tf

x = tf.placeholder(tf.float32, [None, 192])
W = tf.Variable(tf.zeros([192,2]))
b = tf.Variable(tf.zeros([2]))
# y = tf.nn.softmax(tf.matmul(x, W) + b)
y = tf.matmul(x, W) + b
y_ = tf.placeholder(tf.float32, [None,2])

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
# cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y)
# cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
init = tf.initialize_all_variables()

sess = tf.InteractiveSession()
sess.run(init)

BATCH_SIZE = 10
for _i in range(1000):
    batch_start = _i * BATCH_SIZE
    batch_end = batch_start + BATCH_SIZE
    if batch_start > len(train_X) or batch_end>len(train_X):
        print("not enough data!")
        break
    sess.run(train_step, feed_dict={x: train_X[batch_start:batch_end], y_: train_y[batch_start:batch_end]})
    print ("acc %s" % sess.run(accuracy, feed_dict={x: test_X, y_: test_y}))
    print("          loss %s" % sess.run(cross_entropy, feed_dict={x: train_X[batch_start:batch_end], y_: train_y[batch_start:batch_end]}))
    # if _i % 10 == 0:
        # print("acc %s" % sess.run(accuracy, feed_dict={x:test_X, y_: test_y}))
        # print("          loss %s" % sess.run(cross_entropy, feed_dict={x: train_X[batch_start:batch_end], y_: train_y[batch_start:batch_end]}))

