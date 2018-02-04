from datetime import datetime
import time
import tensorflow as tf
import function
import config

def train():
    with tf.Graph().as_default():
        sess = tf.InteractiveSession()
        global_step = tf.train.get_or_create_global_step()

        for j in range(config.FLAGS.max_steps):
            with tf.device('/cpu:0'):
                images, labels = function.get_inputs(eval_data=False)
            for i in range(images.shape[0]):
                logits = function.inference(images[i])
                loss = function.loss(logits, labels[i])
                train_op = function.train_op(loss, global_step)
                sess.run(tf.initialize_all_variables())
                sess.run(train_op)
            print('aa')
        sess.close()

def main(argv=None):
    train()

if __name__ == '__main__':
    tf.app.run()