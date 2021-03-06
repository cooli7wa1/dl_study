BATCH_SIZE = 100
EPOCH = 100

from dataset import *

train_X, train_y = get_data_set(False)
test_X, test_y = get_data_set(True)
test_fuzzing_X, test_fuzzing_y = get_test_separate_data(True)
test_normal_X, test_normal_y = get_test_separate_data(False)
print(train_X.shape, train_y.shape)
print(test_X.shape, test_y.shape)
print(test_fuzzing_X.shape, test_fuzzing_y.shape)
print(test_normal_X.shape, test_normal_y.shape)

import tensorflow as tf

x = tf.placeholder(tf.float32, [None, 192])

# 1
# W1 = tf.Variable(tf.zeros([192, 32]))
# b1 = tf.Variable(tf.zeros([32]))
# W2 = tf.Variable(tf.zeros([32, 2]))
# b2 = tf.Variable(tf.zeros([2]))

# 2
# W1 = tf.Variable(tf.truncated_normal(shape=[192, 80]))
# b1 = tf.Variable(tf.constant(0.1, shape=[80]))
# W2 = tf.Variable(tf.truncated_normal(shape=[80, 2]))
# b2 = tf.Variable(tf.constant(0.1, shape=[2]))

# y1 = tf.matmul(x, W1) + b1
# a1 = tf.nn.relu(y1)
# y2 = tf.matmul(a1, W2) + b2
# a2 = tf.nn.relu(y2)
# y = a2

# y1 = tf.matmul(x, W1) + b1
# y2 = tf.matmul(y1, W2) + b2
# y = y2

# 3
W = tf.Variable(tf.zeros([192, 2]))
b = tf.Variable(tf.zeros([2]))
y = tf.matmul(x, W) + b

y_ = tf.placeholder(tf.float32, [None,2])

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
# cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y)
# cross_entropy = -tf.reduce_sum(y_*tf.log(y))
# cross_entropy = tf.reduce_sum(-y_*tf.log(y)-(1-y_)*tf.log(1-y))
train_step = tf.train.GradientDescentOptimizer(0.0001).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
init = tf.initialize_all_variables()

sess = tf.InteractiveSession()
sess.run(init)

n = len(train_X)
data_mini_batches = [
    train_X[k:k + BATCH_SIZE]
    for k in range(0, n, BATCH_SIZE)]
label_mini_batches = [
    train_y[k:k + BATCH_SIZE]
    for k in range(0, n, BATCH_SIZE)]

for i in range(EPOCH):
    for j in range(len(data_mini_batches)):
        sess.run(train_step, feed_dict={x: data_mini_batches[j],
                                        y_: label_mini_batches[j]})
        loss = sess.run(cross_entropy, feed_dict={x: data_mini_batches[j],
                                        y_: label_mini_batches[j]})
        var_y = sess.run(y, feed_dict={x: data_mini_batches[j],
                                        y_: label_mini_batches[j]})
        acc_test = sess.run(accuracy, feed_dict={x: test_X, y_: test_y})
        acc_test_fuzzing = sess.run(accuracy, feed_dict={x: test_fuzzing_X, y_: test_fuzzing_y})
        acc_test_normal = sess.run(accuracy, feed_dict={x: test_normal_X, y_: test_normal_y})
        acc_train = sess.run(accuracy, feed_dict={x: train_X, y_: train_y})
        # print("acc_test %s, acc_test_fuzzing %s, acc_test_normal %s, acc_train %s, loss %s" %
        #       (acc_test, acc_test_fuzzing, acc_test_normal, acc_train, loss))
        # print("acc_test %s, acc_train %s" % (acc_test, acc_train))
        print("var_y %s, acc_test %s, acc_train %s" % (var_y, acc_test, acc_train))

