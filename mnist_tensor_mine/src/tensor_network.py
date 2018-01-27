import tensorflow as tf
import random
import numpy as np

def SGD_tensor(training_data, epochs, mini_batch_size, eta, test_data=None):
    sess = tf.InteractiveSession()

    x1 = tf.placeholder("float", shape=[None, 784])
    y_ = tf.placeholder("float", shape=[None, 10])

    W1 = tf.Variable(tf.truncated_normal([784, 30], stddev=0.1))
    b1 = tf.Variable(tf.constant(0.1, shape=[30]))
    W2 = tf.Variable(tf.truncated_normal([30, 10], stddev=0.1))
    b2 = tf.Variable(tf.constant(0.1, shape=[10]))

    sess.run(tf.global_variables_initializer())

    y1 = tf.nn.sigmoid(tf.matmul(x1, W1) + b1)
    y2 = tf.nn.sigmoid(tf.matmul(y1, W2) + b2)

    cost = tf.reduce_mean(tf.square(y2-y_))
    train_step = tf.train.GradientDescentOptimizer(eta).minimize(cost)

    test_b1 = np.row_stack(n[0].reshape([1, 784]) for n in test_data)
    test_b2 = np.row_stack(n[1].reshape([1, 10]) for n in test_data)
    test_batches = [test_b1, test_b2]

    n = len(training_data)
    for j in range(epochs):
        random.shuffle(training_data)
        mini_batches_origin = [training_data[k:k + mini_batch_size]
            for k in range(0, n, mini_batch_size)]

        for mini_batch_origin in mini_batches_origin:
            train_b1 = np.row_stack(n[0].reshape([1, 784]) for n in mini_batch_origin)
            train_b2 = np.row_stack(n[1].reshape([1, 10]) for n in mini_batch_origin)
            mini_batches = [train_b1, train_b2]
            train_step.run(feed_dict={x1: mini_batches[0], y_: mini_batches[1]})

        correct_prediction = tf.equal(tf.argmax(y2, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        print("%d: %s" % (j ,accuracy.eval(feed_dict={x1: test_batches[0], y_: test_batches[1]})))
