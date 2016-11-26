import tensorflow as tf
import numpy as np

data = np.loadtxt('new.txt', unpack = True, dtype = 'float32')

print data

xdata = np.transpose(data[0:185])
ydata = np.transpose(data[185:])

print xdata
print ydata

X = tf.placeholder("float", [None, 185])
Y = tf.placeholder("float", [None, 75])

W = tf.Variable(tf.zeros([185, 75]), name="W")

hypothesis = tf.nn.softmax(tf.matmul(X, W))
saver = tf.train.Saver()
learning_rate = 0.0001408

cost = tf.reduce_mean(-tf.reduce_sum(Y*tf.log(hypothesis), reduction_indices = 1))

optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

init = tf.initialize_all_variables()

with tf.Session() as sess:
	sess.run(init)
	
	for step in xrange(2001):
		sess.run(optimizer, feed_dict={X:xdata, Y:ydata})
		if step % 100 == 0:
			print step, sess.run(cost, feed_dict = {X:xdata, Y:ydata}), sess.run(W)
	saver.save(sess, "model.ckpt")
	
	a = sess.run(hypothesis, feed_dict={X:[[1, -77, -59, -73, -80, -50, -52, -61, -64, -58, -70, -77, -75, -78, -82, -74, -81, -51, -75, -73, -62, -57, -81, -80, -84, -87, -82, -67, -72, -85, -76, -81, -75, -79, -82, -64, -79, -74, -82, -85, -80, -75, -78, -85, -85, -83, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130, -130]]})
	
	print a, sess.run(tf.arg_max(a, 1))
