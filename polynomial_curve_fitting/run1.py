"""Simple tutorial for using TensorFlow to compute polynomial regression.
Parag K. Mital, Jan. 2016"""
# %% Imports
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

# %% Let's create some toy data
plt.ion()
n_observations = 100
fig, ax = plt.subplots(1, 1)
xs = np.linspace(-3, 3, n_observations)
ys = np.sin(xs) + np.random.uniform(-0.5, 0.5, n_observations)
# ys = np.tan(xs) + np.random.uniform(-0.2, 0.2, n_observations)
ax.scatter(xs, ys)
fig.show()
plt.draw()

xs = xs.reshape([n_observations, 1]).repeat(INPUT_NUM, 1)
ys = ys.reshape([n_observations, 1])

print(xs.shape, ys.shape)

# %% tf.placeholders for the input and output of the network. Placeholders are
# variables which we need to fill in when we are ready to compute the graph.
X = tf.placeholder(tf.float32, shape=[None, INPUT_NUM])
Y = tf.placeholder(tf.float32, shape=[None, 1])

W1 = weight_variable([INPUT_NUM, 100])
b1 = bias_variable([100])
y1 = tf.matmul(X, W1) + b1
# a1 = tf.nn.sigmoid(y1)
a1 = tf.nn.tanh(y1)
# a1 = y1

# 1
W2 = weight_variable([100, 1])
b2 = bias_variable([1])
y2 = tf.matmul(a1, W2) + b2
# a2 = tf.nn.sigmoid(y2)
a2 = tf.nn.tanh(y2)

# 2
# W2 = weight_variable([1000, 1])
# b2 = bias_variable([1])
# y2 = tf.matmul(a1, W2) + b2
# # a2 = tf.nn.sigmoid(y2)
# # a2 = tf.nn.tanh(y2)


# W3 = weight_variable([32, 1])
# b3 = bias_variable([1])
# y3 = tf.matmul(a2, W3) + b3
# # a3 = tf.nn.sigmoid(y3)
# a3 = tf.nn.tanh(y3)

Y_pred = a2

# %% Loss function will measure the distance between our observations
# and predictions and average over them.
cost = tf.reduce_sum(tf.pow(Y_pred - Y, 2)) / (n_observations - 1)
# cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=Y_pred))

# %% if we wanted to add regularization, we could add other terms to the cost,
# e.g. ridge regression has a parameter controlling the amount of shrinkage
# over the norm of activations. the larger the shrinkage, the more robust
# to collinearity.
# cost = tf.add(cost, tf.mul(1e-6, tf.global_norm([W])))

# %% Use gradient descent to optimize W,b
# Performs a single step in the negative gradient
learning_rate = 0.1
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# %% We create a session to use the graph
n_epochs = 10000
with tf.Session() as sess:
    # Here we tell tensorflow that we want to initialize all
    # the variables in the graph so we can use them
    sess.run(tf.global_variables_initializer())

    # Fit all training data
    prev_training_cost = 0.0
    for epoch_i in range(n_epochs):
        for i in range(n_observations):
            sess.run(optimizer, feed_dict={X: xs[i:(i+1)], Y: ys[i:(i+1)]})

        training_cost = sess.run(
            cost, feed_dict={X: xs, Y: ys})
        print(training_cost)

        if epoch_i % 10 == 0:
            ax.plot(xs, Y_pred.eval(feed_dict={X: xs}, session=sess),
                    'k', alpha=1)
            fig.show()
            plt.draw()

        # Allow the training to quit if we've reached a minimum
        if np.abs(prev_training_cost - training_cost) < 0.00001:
            break
        # if np.abs(training_cost) < 0.05:
        #     break
        prev_training_cost = training_cost
ax.set_ylim([-3, 3])
fig.show()
plt.waitforbuttonpress()