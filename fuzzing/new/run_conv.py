BATCH_SIZE = 100
EPOCH = 100

from dataset import get_data_set

train_X, train_y = get_data_set(False)
test_X, test_y = get_data_set(True)
print(train_X.shape, train_y.shape)
print(test_X.shape, test_y.shape)

import tensorflow as tf

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv1d(x, W, 1, padding='SAME')

def max_pool_2x2(x):
  return tf.nn.pool(x, [2], 'MAX', 'SAME', strides=[2])

x = tf.placeholder(tf.float32, shape=[None, 192])
y_ = tf.placeholder(tf.float32, shape=[None, 2])

W_conv1 = weight_variable([7, 1, 16])
b_conv1 = bias_variable([16])
x_image = tf.reshape(x, [-1, 192, 1])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([7, 16, 32])
b_conv2 = bias_variable([32])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([48 * 32, 16])
b_fc1 = bias_variable([16])
h_pool2_flat = tf.reshape(h_pool2, [-1, 48 * 32])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([16, 2])
b_fc2 = bias_variable([2])

# y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
# cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))

y_conv=tf.matmul(h_fc1_drop, W_fc2) + b_fc2
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
train_step = tf.train.AdamOptimizer(0.0001).minimize(cross_entropy)
# train_step = tf.train.GradientDescentOptimizer(1e-5).minimize(cross_entropy) # 1e-5 0.006

correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
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
        sess.run(train_step, feed_dict={x: data_mini_batches[i],
                                        y_: label_mini_batches[i],
                                        keep_prob: 0.5})
        loss = sess.run(cross_entropy, feed_dict={x: data_mini_batches[i],
                                        y_: label_mini_batches[i],
                                        keep_prob: 0.5})
        acc_test = sess.run(accuracy, feed_dict={x: test_X, y_: test_y, keep_prob: 1.0})
        acc_train = sess.run(accuracy, feed_dict={x: train_X, y_: train_y, keep_prob: 1.0})
        # print("acc_test %s, acc_train %s, loss %s" % (acc_test, acc_train, loss))
        print("acc_test %s, acc_train %s" % (acc_test, acc_train))

