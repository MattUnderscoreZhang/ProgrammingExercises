import tensorflow as tf
import numpy as np

N_NODES = 3
nodes = [(0,0), (0.5,0.5), (0,1)]

# shoelace formula
x = tf.placeholder(tf.float32)
y = tf.placeholder(tf.float32)
x_roll_1 = tf.concat(values=[x[N_NODES-1:], x[:N_NODES-1]], concat_dim=0)
y_roll_1 = tf.concat(values=[y[N_NODES-1:], y[:N_NODES-1]], concat_dim=0)
shoelace_x = tf.reduce_sum(tf.multiply(x, y_roll_1))
shoelace_y = tf.reduce_sum(tf.multiply(y, x_roll_1))
area = tf.constant(0.5) * tf.abs(shoelace_x - shoelace_y)

with tf.Session() as sess:
    print("Area is", sess.run(area, feed_dict={x : [x[0] for x in nodes], y : [x[1] for x in nodes]}))
