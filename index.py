import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
if __name__ == '__main__':
    x_data = np.linspace(-0.5, 0.5, 100)[:, np.newaxis]
    x_value = np.linspace(-0.5, 0.5, 1000)[:, np.newaxis]
    noise = np.random.normal(0, 0.01, x_data.shape)
    y_data = np.square(x_data) + noise

    x = tf.placeholder(tf.float32, [None, 1])
    y = tf.placeholder(tf.float32, [None, 1])

    Initial_Weight = tf.random_normal([1, 10])
    Initial_Bias = tf.zeros([1, 10])

    Initial_Out_Weight = tf.random_normal([10, 1])
    Initial_Out_Bias = tf.zeros([1, 1])
    Weights_L1 = tf.Variable(Initial_Weight)
    bias_L1 = tf.Variable(Initial_Bias)
    Wx_plus_b_L1 = tf.matmul(x, Weights_L1) + bias_L1
    L1 = tf.nn.relu(Wx_plus_b_L1)

    Weights_L2 = tf.Variable(Initial_Out_Weight)
    bias_L2 = tf.Variable(Initial_Out_Bias)
    prediction = tf.matmul(L1, Weights_L2) + bias_L2

    loss = tf.reduce_mean(tf.reduce_sum(tf.square(y-prediction), reduction_indices=[1]))
    train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for _ in range(1000):
            sess.run(train_step, feed_dict={x: x_data, y: y_data})

        prediction_value = sess.run(prediction, feed_dict={x: x_value})
        plt.scatter(x_data, y_data)
        plt.plot(x_value, prediction_value, 'r-')
        plt.show()