import mnist_loader
import network
import tensor_network
import datetime

time_s = datetime.datetime.now()

training_data, validation_data, test_data = \
    mnist_loader.load_data_wrapper()

# for origin
# net = network.Network([784, 30, 10])
# net.SGD(training_data, 30, 20, 3.0, test_data=test_data)

# for tensorflow
tensor_network.SGD_tensor(training_data, 30, 20, 3, test_data=test_data)

time_e = datetime.datetime.now()

print("total time: %s" % (time_e-time_s))