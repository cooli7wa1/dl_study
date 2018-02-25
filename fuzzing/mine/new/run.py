from dataset import get_data_set
train_X, train_y = get_data_set(False)
test_X, test_y = get_data_set(True)
print(train_X.shape, train_y.shape)
print(test_X.shape, test_y.shape)

import tensorflow as tf

x = tf.placeholder(tf.float32, [None, 192])
W = tf.Variable(tf.zeros([192,2]))
b = tf.Variable(tf.zeros([2]))
# W = tf.Variable(tf.truncated_normal(shape=[192,2]))
# b = tf.Variable(tf.constant(0.1, shape=[2]))
# y = tf.nn.softmax(tf.matmul(x, W) + b)
y = tf.matmul(x, W) + b
y_ = tf.placeholder(tf.float32, [None,2])

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
# cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y)
# cross_entropy = -tf.reduce_sum(y_*tf.log(y))
# cross_entropy = tf.reduce_sum(-y_*tf.log(y)-(1-y_)*tf.log(1-y))
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
    var = sess.run(y, feed_dict={x: train_X[batch_start:batch_end], y_: train_y[batch_start:batch_end]})
    sess.run(train_step, feed_dict={x: train_X[batch_start:batch_end], y_: train_y[batch_start:batch_end]})
    if _i % 10 == 0:
        acc = sess.run(accuracy, feed_dict={x: test_X, y_: test_y})
        loss = sess.run(cross_entropy, feed_dict={x: train_X[batch_start:batch_end],
                                                  y_: train_y[batch_start:batch_end]})
        print("acc %s loss %s" % (acc, loss))

