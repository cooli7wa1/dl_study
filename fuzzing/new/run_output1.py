BATCH_SIZE = 1000
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

# for i in range(10):
#     print(train_y[i])

import tensorflow as tf

x = tf.placeholder(tf.float32, [None, 192])

# 1
# W1 = tf.Variable(tf.zeros([192, 32]))
# b1 = tf.Variable(tf.zeros([32]))
# W2 = tf.Variable(tf.zeros([32, 2]))
# b2 = tf.Variable(tf.zeros([2]))

# 2
W1 = tf.Variable(tf.truncated_normal(shape=[192, 80]))
b1 = tf.Variable(tf.constant(0.1, shape=[80]))
W2 = tf.Variable(tf.truncated_normal(shape=[80, 2]))
b2 = tf.Variable(tf.constant(0.1, shape=[2]))

y1 = tf.matmul(x, W1) + b1
y2 = tf.matmul(y1, W2) + b2
y = tf.abs(y2)

# 3
# W = tf.Variable(tf.zeros([192, 2]))
# b = tf.Variable(tf.zeros([2]))
# W = tf.Variable(tf.truncated_normal(shape=[192, 2]))
# b = tf.Variable(tf.constant(0.1, shape=[2]))
# y = tf.matmul(x, W) + b
# y = tf.abs(y)

y_ = tf.placeholder(tf.float32, [None,2])

y_0 = y[:, 0]
y_1 = y[:, 1]
y_prop = tf.divide(y_1, tf.add(y_0, y_1))  # fuzzing prop
y_prop_ = y_[:, 0]  # normal number 0 or 1

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.train.GradientDescentOptimizer(0.0001).minimize(cross_entropy)

correct_prediction = tf.equal(tf.cast(tf.less(y_prop, 0.85), tf.float32), y_prop_)
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
        acc_test = sess.run(accuracy, feed_dict={x: test_X, y_: test_y})
        # acc_train = sess.run(accuracy, feed_dict={x: train_X, y_: train_y})

        var_y, var_y_0, var_y_1, var_y_prop, var_y_prop_ = sess.run((y, y_0, y_1, y_prop, y_prop_), feed_dict={x: data_mini_batches[j],
                                        y_: label_mini_batches[j]})

        acc_test_fuzzing = sess.run(accuracy, feed_dict={x: test_fuzzing_X, y_: test_fuzzing_y})
        acc_test_normal = sess.run(accuracy, feed_dict={x: test_normal_X, y_: test_normal_y})
        # print("acc_test %s, acc_test_fuzzing %s, acc_test_normal %s, loss %s" %
        #       (acc_test, acc_test_fuzzing, acc_test_normal, loss))
        print("acc_test_fuzzing %s, acc_test_normal %s, loss %s" %
              (acc_test_fuzzing, acc_test_normal, loss))
        # print("acc_test %s, acc_train %s, y %s, loss %s" % (acc_test, acc_train, var_y, loss))
        # print("acc_test %s, acc_train %s, loss %s" % (acc_test, acc_train, loss))
        # print("acc_test %s, loss %s, y %s" % (acc_test, loss, var_y))
        # print("y %s ,y_0 %s, y_1 %s, y_prop %s, y_prop_ %s" % (var_y, var_y_0, var_y_1, var_y_prop, var_y_prop_))

