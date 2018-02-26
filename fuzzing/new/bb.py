import tensorflow as tf


a = tf.Variable([[1,1],[2,2]], dtype=tf.float32)
b_0 = a[:, 0]
b_1 = a[:, 1]
b = tf.divide(b_0, tf.add(b_0, b_1))

sess = tf.InteractiveSession()
sess.run(tf.initialize_all_variables())

print(sess.run(b))