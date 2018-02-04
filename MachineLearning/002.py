import tensorflow as tf
import numpy.random as rand
import matplotlib.pyplot as plt

# solve x^3 - log(x^2) + 3 = 0
x = tf.Variable(rand.randn())
function = abs(tf.subtract(tf.pow(x,3), tf.log(tf.pow(x,2))) + 3)

learning_rate = 0.01
epochs = 500

optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(function)

history = []
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for epoch in range(epochs):
        sess.run(optimizer)
        history.append(sess.run(x))
print("x =", history[-1])
plt.plot(range(len(history)), history)
plt.show()
