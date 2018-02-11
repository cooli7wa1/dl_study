import tensorflow as tf
import numpy as np

img2 = np.random.randint(255, size=(10,224,224,3))
img1 = np.random.randint(255, size=(224,224,3))
image = tf.placeholder(tf.float32, shape=[None, 224, 224, 3], name='input_image')
output = tf.size(image)

with tf.Session() as sess:
    print(sess.run(output, feed_dict={image: img2}))
    print(sess.run(output, feed_dict={image: img1}))