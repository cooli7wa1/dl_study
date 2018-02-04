import tensorflow as tf

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_integer('max_steps', 10,
                            """Number of batches to run.""")
tf.app.flags.DEFINE_integer('data_size', 192,
                            """data length""")
tf.app.flags.DEFINE_integer('label_size', 1,
                            """label length""")
tf.app.flags.DEFINE_integer('batch_size', 10,
                            """batch_size""")
tf.app.flags.DEFINE_integer('capacity', 30,
                            """capacity""")
tf.app.flags.DEFINE_integer('min_after_dequeue', 20,
                            """min_after_dequeue""")
tf.app.flags.DEFINE_integer('learning_rate', 1,
                            """learning_rate""")

tf.app.flags.DEFINE_string('data_dir', 'E:\\PycharmProjects\\dl_study\\fuzzing\\data\\',
                           """data directory""")
tf.app.flags.DEFINE_string('train_data', 'mix_train_24000.dat',
                           """train data""")
tf.app.flags.DEFINE_string('test_data', 'mix_test_6000.dat',
                           """test data""")

