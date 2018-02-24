import mnist_loader
import network
import datetime

time_load_s = datetime.datetime.now()
training_data, validation_data, test_data = \
    mnist_loader.load_data_wrapper()
time_load_e = datetime.datetime.now()
print("load time: %s" % (time_load_e-time_load_s))

net = network.Network([784, 20, 10])

time_train_s = datetime.datetime.now()
net.SGD(training_data, 30, 1, 3.0, test_data=test_data)
time_train_e = datetime.datetime.now()

print("load time: %s" % (time_load_e-time_load_s))
print("train time: %s" % (time_train_e-time_train_s))