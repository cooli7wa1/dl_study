import tensorflow as tf


a = tf.Variable([[1]*10], dtype=tf.float32)
a = tf.reshape(a, [1, -1])
b = tf.nn.softmax(a)
b = tf.reshape(b, [-1, 1])

sess = tf.InteractiveSession()
sess.run(tf.initialize_all_variables())

print(sess.run(b))