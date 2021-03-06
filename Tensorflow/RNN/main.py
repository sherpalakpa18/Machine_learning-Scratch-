import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
# from tensorflow.python.ops import rnn, rnn_cell
from tensorflow.contrib import rnn 

mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

hm_epochs = 50
n_classes = 10
#batch size is number of image in i/p at a time
batch_size = 128

#Chunk size of our image
chunk_size = 28
n_chunks = 28
rnn_size = 128

#Height x width  # input feature size = 28x28 pixels = 784
x = tf.placeholder('float', [None, n_chunks, chunk_size])
y = tf.placeholder('float')

def reccurrent_network_network(x):
	layer = {'weights':tf.Variable(tf.random_normal([rnn_size,n_classes])),
			'biases':tf.Variable(tf.random_normal([n_classes	]))}
						
	# Refer transpose.py for transpose
	x = tf.transpose(x, [1,0,2])
	x = tf.reshape(x, [-1, chunk_size])
	# x = tf.split(0, n_chunks, x) 
	x = tf.split(x, n_chunks, 0)

	# lstm_cell = rnn_cell.BasicLSTMCell(rnn_size)
	# outputs, states = rnn.rnn(lstm_cell, x, dtype=float32)
	lstm_cell = rnn.BasicLSTMCell(rnn_size)
	outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)


	output = tf.matmul(outputs[-1], layer['weights']) + layer['biases']

	return output

def train_neural_network(x):
	prediction = reccurrent_network_network(x)
	 # OLD VERSION:
    #cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(prediction,y) )
    # NEW:
	cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y) )
	optimizer = tf.train.AdamOptimizer().minimize(cost)

	# Add ops to save and restore all the variables.
	saver = tf.train.Saver()


	with tf.Session() as sess:
		# OLD:
        #sess.run(tf.initialize_all_variables())
        # NEW:
		# sess.run(tf.global_variables_initializer())

		# for epoch in range(hm_epochs):
		# 	epoch_loss = 0
		# 	for _ in range(int(mnist.train.num_examples/batch_size)):
		# 		epoch_x, epoch_y = mnist.train.next_batch(batch_size)
		# 		epoch_x = epoch_x.reshape(batch_size, n_chunks, chunk_size)

		# 		_, c = sess.run([optimizer, cost], feed_dict = {x: epoch_x, y:epoch_y})
		# 		epoch_loss += c

		# 	print('Epoch',epoch,'completed out of ', hm_epochs,'loss: ',epoch_loss)
			
		saver = tf.train.import_meta_graph('/tmp/model.ckpt.meta')
		saver.restore(sess, "/tmp/model.ckpt")

		correct = tf.equal(tf.argmax(prediction,1), tf.argmax(y,1))

		accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

		print('Accuracy:',accuracy.eval({x:mnist.test.images.reshape(-1, n_chunks, chunk_size), y:mnist.test.labels}))

		# save_path = saver.save(sess, "/tmp/model.ckpt")
		# print("Model saved in file: %s" % save_path)

train_neural_network(x)