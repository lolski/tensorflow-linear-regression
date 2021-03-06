import csv
import plotly
import plotly.graph_objs as g
import tensorflow as tf


def read_csv_file(path, skip_first_line):
    with open(path) as file:
        reader = csv.reader(file)

        if skip_first_line:
            next(reader, None)

        accumulator = []
        for row in reader:
            accumulator.append(row)

        return accumulator


# ------------------ main ------------------
# step 1: model y = mx + b
y = tf.placeholder(tf.float32, name='y')
m = tf.Variable(0.0, name='slope')
x = tf.placeholder(tf.float32, name='x')
b = tf.Variable(0.0, name='offset')
y_predicted = m*x+b

# step 2: read csv
data = read_csv_file('res/train.csv', True)

# step 3: apply gradient descent optimizer in order to find m and b
num_of_epochs = 100
learning_rate=0.00001
loss_fn = tf.square(y - y_predicted, name='loss')
loss_fn_with_logs = tf.Print(loss_fn, [loss_fn, m, b])
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss_fn_with_logs)
with tf.Session() as s:
    s.run(tf.global_variables_initializer())
    print('training starts...')
    for i in range(num_of_epochs):
        for row in data:
            row_x, row_y = row
            s.run(optimizer, feed_dict={x: row_x, y: row_y})
        print('i=' + str(i))
    m_value, b_value = s.run([m, b])

    print('training has ended. m=' + str(m_value) + ', ' + str(b_value))

# step 4: plot
data_plot = {
    'x_axis': list(map(lambda e: e[0], data)),
    'y_axis': list(map(lambda e: e[1], data))
}
y_predicted_plot = {
    'x_axis': [0, 100],
    'y_axis': [0, m_value*100 + b_value]
}
plotly.offline.plot({
    'data': [
        g.Scatter(x=data_plot['x_axis'], y=data_plot['y_axis'], mode='markers'),
        g.Scatter(x=y_predicted_plot['x_axis'], y=y_predicted_plot['y_axis'])
    ]
})