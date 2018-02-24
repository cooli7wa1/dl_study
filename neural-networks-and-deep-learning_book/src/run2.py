import mnist_loader
import network2
import datetime

time_load_s = datetime.datetime.now()
training_data, validation_data, test_data = \
    mnist_loader.load_data_wrapper()
time_load_e = datetime.datetime.now()
print("load time: %s" % (time_load_e-time_load_s))

net = network2.Network([784, 30, 30, 10], cost=network2.CrossEntropyCost)
net.large_weight_initializer()

time_train_s = datetime.datetime.now()
net.SGD(training_data, 30, 10, 0.1,
        evaluation_data=validation_data,
        monitor_evaluation_accuracy=True,
        lmbda=5.0)
time_train_e = datetime.datetime.now()

print("load time: %s" % (time_load_e-time_load_s))
print("load time: %s" % (time_train_e-time_train_s))