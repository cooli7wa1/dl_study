import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


money=np.array([[109],[82],[99], [72], [87], [78], [86], [84], [94], [57]]).astype(np.float32)
click=np.array([[11], [8], [8], [6],[ 7], [7], [7], [8], [9], [5]]).astype(np.float32)

X_test = money[0:5].reshape(-1,1)
y_test = click[0:5]
X_train = money[5:].reshape(-1,1)
y_train = click[5:]

x=tf.placeholder(tf.float32,[None,1])
W=tf.Variable(tf.zeros([1,1]))
b=tf.Variable(tf.zeros([1]))

y=tf.matmul(x,W)+b

y_=tf.placeholder(tf.float32,[None,1])

cost=tf.reduce_sum(tf.pow((y_-y),2))
train_step=tf.train.GradientDescentOptimizer(0.000001).minimize(cost)

init=tf.global_variables_initializer()
sess=tf.Session()
sess.run(init)

cost_history=[]

for i in range(100):
    feed={x:X_train,y_:y_train}
    sess.run(train_step,feed_dict=feed)
    cost_history.append(sess.run(cost,feed_dict=feed))
    print("After %d iteration:" %i)
    # print("W: %f" % sess.run(W))
    # print("b: %f" % sess.run(b))
    print("cost: %f" % sess.run(cost,feed_dict=feed))
print("W_Value: %f" % sess.run(W),"b_Value: %f" % sess.run(b),"cost_Value: %f" % sess.run(cost,feed_dict=feed))

plt.plot(range(len(cost_history)),cost_history)
plt.axis([0,100,0,np.max(cost_history)])
plt.xlabel('training epochs')
plt.ylabel('cost')
plt.title('cost history')
plt.show()