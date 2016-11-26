import tensorflow as tf
import numpy as np

data = np.loadtxt('data.txt', unpack = True, dtype = 'float32')

print data

xdata = np.transpose(data[0:3])
ydata = np.transpose(data[3:])

print xdata
print ydata

X = tf.placeholder("float", [None, 3])
Y = tf.placeholder("float", [None, 3])

W = tf.Variable(tf.zeros([3, 3]))

hypothesis = tf.nn.softmax(tf.matmul(X, W))

learning_rate = 0.001

cost = tf.reduce_mean(-tf.reduce_sum(Y*tf.log(hypothesis), reduction_indices = 1))

optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

init = tf.initialize_all_variables()

with tf.Session() as sess:
	sess.run(init)
	
	for step in xrange(2001):
		sess.run(optimizer, feed_dict={X:xdata, Y:ydata})
		if step % 100 == 0:
			print step, sess.run(cost, feed_dict = {X:xdata, Y:ydata}), sess.run(W)
	