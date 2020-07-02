import tensorflow as tf

mnist = tf.keras.datasets.mnist

(trans_images, trans_labels), (test_images, test_labels) = mnist.load_data()
print(trans_images[1].shape)


# oad_image(trans_images[5])

total_num = len(trans_images)
valid_split = 0.2  # 验证集的比例占20%
train_num = int(total_num * (1 - valid_split))
# 前部分分给训练集
tran_x = trans_images[:train_num]
tran_y = trans_labels[:train_num]
# 后部分分给验证集 20%
valid_x = trans_images[train_num:]
valid_y = trans_labels[train_num:]
# 测试集 1万条
test_x = test_images
test_y = test_labels

# print(tran_x.shape)
# (48000, 28, 28)

# 把（28 ， 28）的结构拉直为一行 784
tran_x = tran_x.reshape(-1, 784)
# print(tran_x.shape)
# (48000, 784)
valid_x = valid_x.reshape(-1, 784)
test_x = test_x.reshape(-1, 784)

# 特征数据归一化

tran_x = tf.cast(tran_x / 255.0, tf.float32)
valid_x = tf.cast(valid_x / 255.0, tf.float32)
test_x = tf.cast(test_x / 255.0, tf.float32)

# 独热编码
tran_y = tf.one_hot(tran_y, depth=10)
valid_y = tf.one_hot(valid_y, depth=10)
test_y = tf.one_hot(test_y, depth=10)
print(tran_y[1])


# tf.Tensor([1. 0. 0. 0. 0. 0. 0. 0. 0. 0.], shape=(10,), dtype=float32)

# 定义模型
def model(x, w, b):
    pred = tf.matmul(x, w) + b
    # 对tf.nn.softmax的理解
    # https://blog.csdn.net/wgj99991111/article/details/83586508
    return tf.nn.softmax(pred)


# 创建变量
W = tf.Variable(tf.random.normal([784, 10], mean=0.0, stddev=1.0, dtype=tf.float32))
B = tf.Variable(tf.zeros([10]), dtype=tf.float32)


# 定义损失函数-交叉熵

def loss(x, y, w, b):
    # 计算预测值
    pred = model(x, w, b)
    loss_ = tf.keras.losses.categorical_crossentropy(y_true=y, y_pred=pred)
    return tf.reduce_mean(loss_)  # 求均值，得出均方差


# 定义超参数
training_epochs = 30  # 训练轮次
batch_size = 50  # 单次训练样本数 批次大小
learning_rate = 0.001


# 定义梯度计算函数
def grad(x, y, w, b):
    with tf.GradientTape() as tape:
        loss_ = loss(x, y, w, b)
    return tape.gradient(loss_, [w, b])


# 选择优化器
# adam 优化器

optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)


# 定义准确率
def accuracy(x, y, w, b):
    pred = model(x, w, b)
    # 预测值和实际值匹配
    corrent_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    # 准确率，布尔值转换为浮点值，并且计算平均值
    return tf.reduce_mean(tf.cast(corrent_prediction, tf.float32))


# 模型训练
total_step = int(train_num / batch_size)
loss_list_train = []
loss_list_valid = []
acc_list_train = []  # 用于保存训练集acc值列表
acc_list_valid = []  # 验证acc列表

for epoch in range(training_epochs):
    for step in range(total_step):
        xs = tran_x[step * batch_size:(step + 1) * batch_size]
        ys = tran_y[step * batch_size:(step + 1) * batch_size]

        grads = grad(xs, ys, W, B)  # 计算梯度
        optimizer.apply_gradients(zip(grads, [W, B]))
    loss_train = loss(tran_x, tran_y, W, B).numpy()  # 计算当前轮次训练损失
    loss_valid = loss(valid_x, valid_y, W, B).numpy()
    acc_train = accuracy(tran_x, tran_y, W, B).numpy()
    acc_valid = accuracy(valid_x, valid_y, W, B).numpy()
    loss_list_train.append(loss_train)
    loss_list_valid.append(loss_valid)
    acc_list_train.append(acc_train)
    acc_list_valid.append(acc_valid)
    print('epoch={:3d},train_lost={:.4f},train_acc={:.4f},val_loss{:.4f},val_acc={:.4f}'.format(
        epoch + 1, loss_train, acc_train, loss_valid, acc_valid
    ))

# 评估模型，在测试集上评估模型的准确率
acc_test = accuracy(test_x, test_y, W, B).numpy()
print('test Accurace:', acc_test)