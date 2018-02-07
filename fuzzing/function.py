import input_data
import tensorflow as tf
from config import FLAGS

def _get_variable(name, shape, initializer):
    with tf.device('/cpu:0'):
        return tf.get_variable(name, shape, initializer=initializer, dtype=tf.float32)

def get_inputs(eval_data):
    if eval_data:
        file_list = [FLAGS.data_dir + FLAGS.test_data]
    else:
        file_list = [FLAGS.data_dir + FLAGS.train_data]
    images, labels = input_data.input(file_list)
    return images, labels

def inference(images):
    w1 = _get_variable('weights1', [192, 32],
                       tf.truncated_normal_initializer(stddev=0.1, dtype=tf.float32))
    b1 = _get_variable('biases1', [32], tf.constant_initializer(0.1))
    out1 = tf.nn.relu(tf.matmul(images, w1) + b1, name='layer1')
    w2 = _get_variable('weights2', [32, 2],
                       tf.truncated_normal_initializer(stddev=0.1, dtype=tf.float32))
    b2 = _get_variable('biases2', [2], tf.constant_initializer(0.1))
    out2 = tf.nn.relu(tf.matmul(out1, w2) + b2, name='layer2')
    return out2

def loss(logits, labels):
    softmax = tf.nn.softmax(logits)
    print("logits: %s"%logits.shape)
    print("labels: %s"%labels.shape)
    print("softmax: %s"%softmax.shape)
    # cross_entropy = -tf.reduce_sum(labels*tf.log(softmax+(1e-8)))
    cross_entropy = -tf.reduce_sum(labels*tf.log(softmax))
    cross_entropy_mean = tf.reduce_mean(cross_entropy, name='cross_entropy')
    return cross_entropy_mean

    # labels = tf.reshape(labels, [10,])
    # cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
    #     labels=labels, logits=logits, name='cross_entropy_per_example')
    # cross_entropy_mean = tf.reduce_mean(cross_entropy, name='cross_entropy')
    # return cross_entropy_mean

def train_op(total_loss, global_step):
    opt = tf.train.GradientDescentOptimizer(FLAGS.learning_rate)
    grads = opt.compute_gradients(total_loss)
    apply_gradient_op = opt.apply_gradients(grads, global_step=global_step)
    return apply_gradient_op