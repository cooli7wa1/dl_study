from datetime import datetime
import time
import tensorflow as tf
import function
import config

def train():
    with tf.Graph().as_default():
        global_step = tf.train.get_or_create_global_step()

        with tf.device('/cpu:0'):
            images, labels = function.get_inputs(eval_data=False)
        for i in range(images.shape[0]):
            logits = function.inference(images[i])
            loss = function.loss(logits, labels[i])
            train_op = function.train_op(loss, global_step)

        class _LoggerHook(tf.train.SessionRunHook):
            """Logs loss and runtime."""

            def begin(self):
                self._step = -1
                self._start_time = time.time()

            def before_run(self, run_context):
                self._step += 1
                return tf.train.SessionRunArgs(loss)  # Asks for loss value.

            def after_run(self, run_context, run_values):
                if self._step % config.FLAGS.log_frequency == 0:
                    current_time = time.time()
                    duration = current_time - self._start_time
                    self._start_time = current_time

                    loss_value = run_values.results
                    examples_per_sec = config.FLAGS.log_frequency * config.FLAGS.batch_size / duration
                    sec_per_batch = float(duration / config.FLAGS.log_frequency)

                    format_str = ('%s: step %d, loss = %.2f (%.1f examples/sec; %.3f '
                                  'sec/batch)')
                    print(format_str % (datetime.now(), self._step, loss_value,
                                        examples_per_sec, sec_per_batch))

        with tf.train.MonitoredTrainingSession(
                hooks=[tf.train.StopAtStepHook(last_step=config.FLAGS.max_steps),
                       tf.train.NanTensorHook(loss),
                       _LoggerHook()],
                ) as mon_sess:
            while not mon_sess.should_stop():
                mon_sess.run(train_op)

def main(argv=None):
    train()

if __name__ == '__main__':
    tf.app.run()