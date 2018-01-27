import tensorflow as tf
import numpy as np

img = np.random.randint(255, size=(224,224,3))
img = np.reshape(img, (1,224,224,3))
image = tf.placeholder(tf.float32, shape=[None, 224, 224, 3])
output = tf.size(image)

with tf.Session() as sess:
    print(sess.run(output, feed_dict={image: img}))