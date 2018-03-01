import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

INPUT_NUM = 1

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

plt.ion()
n_observations = 100
fig, ax = plt.subplots(1, 1)
xs = np.linspace(-3, 3, n_observations)
ys = np.sin(xs) + np.random.uniform(-0.2, 0.2, n_observations)
ax.scatter(xs, ys)
fig.show()
plt.draw()

xs = xs.reshape([n_observations, 1]).repeat(INPUT_NUM, 1)
ys = ys.reshape([n_observations, 1])

print(xs.shape, ys.shape)

X = tf.placeholder(tf.float32, shape=[None, INPUT_NUM])
Y = tf.placeholder(tf.float32, shape=[None, 1])

W1 = weight_variable([INPUT_NUM, 100])
b1 = bias_variable([100])
y1 = tf.matmul(X, W1) + b1
# a1 = tf.nn.sigmoid(y1)
a1 = tf.nn.tanh(y1)

W2 = weight_variable([100, 1])
b2 = bias_variable([1])
# y2 = tf.matmul(a1, W2) + b2
y2 = tf.matmul(a1, W2)

Y_pred = y2

cost = tf.reduce_sum(tf.pow(Y_pred - Y, 2)) / (n_observations - 1)

learning_rate = 0.1
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

n_epochs = 10000
with tf.Session() as sess:

    sess.run(tf.global_variables_initializer())

    prev_training_cost = 0.0
    for epoch_i in range(n_epochs):
        for i in range(n_observations):
            sess.run(optimizer, feed_dict={X: xs[i:(i+1)], Y: ys[i:(i+1)]})

        training_cost = sess.run(
            cost, feed_dict={X: xs, Y: ys})
        print(training_cost)

        if np.abs(prev_training_cost - training_cost) < 0.00001:
            ax.plot(xs, Y_pred.eval(feed_dict={X: xs}, session=sess),
                    'k', alpha=1)
            fig.show()
            plt.draw()
            break
        prev_training_cost = training_cost

ax.set_ylim([-3, 3])
fig.show()
plt.draw()
plt.waitforbuttonpress()