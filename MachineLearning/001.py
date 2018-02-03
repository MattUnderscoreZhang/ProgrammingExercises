import tensorflow as tf
import numpy.random as rand

###################
# MATH OPERATIONS #
###################

a = tf.constant(3)
b = tf.constant(5)
c = tf.constant(9)

add = tf.add(a,b)
multiply = tf.multiply(a,b)
function = tf.multiply(tf.add(a,b),c)

print("Basic functions")
with tf.Session() as sess:
    print(sess.run(a))
    print(sess.run(add))
    print(sess.run(multiply, feed_dict={b: 12}))
    print(sess.run(function))
print()

a = tf.constant([[5, 2, 1, 4],
                 [3, 8, 2, 9]])
b = tf.constant([[8, 0],
                 [5, 1],
                 [8, 7],
                 [0, 3]])

product = tf.matmul(a,b)

print("Matrix multiplication")
with tf.Session() as sess:
    print(sess.run(product))
print()

###################################
# VARIABLES AND COST MINIMIZATION #
###################################

a = tf.placeholder("float")
b = tf.Variable(rand.randn())
learning_rate = 0.01

cost = abs(tf.subtract(a,b))
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)
    for epoch in range(5000):
        sess.run(optimizer, feed_dict={a: 50})
    print("Value of b:", sess.run(b))
