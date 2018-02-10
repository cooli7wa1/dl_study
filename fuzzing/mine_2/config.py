import tensorflow as tf

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_integer('max_steps', 10000,
                            """Number of batches to run.""")
tf.app.flags.DEFINE_integer('data_size', 192,
                            """data length""")
tf.app.flags.DEFINE_integer('label_size', 2,
                            """label length""")
tf.app.flags.DEFINE_integer('batch_size', 100,
                            """batch_size""")
tf.app.flags.DEFINE_integer('capacity', 20000,
                            """capacity""")
tf.app.flags.DEFINE_integer('min_after_dequeue', 1500,
                            """min_after_dequeue""")
tf.app.flags.DEFINE_integer('learning_rate', 0.01,
                            """learning_rate""")
tf.app.flags.DEFINE_integer('log_frequency', 10,
                            """How often to log results to the console.""")
# tf.app.flags.DEFINE_string('data_dir', 'E:\\PycharmProjects\\dl_study\\fuzzing\\data\\', """data directory""")
tf.app.flags.DEFINE_string('data_dir', '/home/cooli7wa/Documents/dl_study/fuzzing/data/', """data directory""")
# tf.app.flags.DEFINE_string('train_data', 'mix_train_24000.dat',
#                            """train data""")
tf.app.flags.DEFINE_string('train_data', 'mix_train_24000_test.dat',
                           """train data""")
tf.app.flags.DEFINE_string('test_data', 'mix_test_6000_test.dat',
                           """test data""")

