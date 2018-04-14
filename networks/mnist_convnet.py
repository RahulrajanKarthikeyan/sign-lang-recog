from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import pandas as pd
from sklearn import preprocessing

img_width = 28
img_height = 28
train_data_directory = 'data/sign_mnist_train.csv'
validation_data_directory = 'data/sign_mnist_test.csv'
batch_size = 24 * 4
epochs = 10

train = pd.read_csv(train_data_directory).values
test = pd.read_csv(validation_data_directory).values

if K.image_data_format() == 'channels_first':
    trainX = train[:, 1:].reshape(train.shape[0], 1, 28, 28).astype('float32')
    testX = test[:, 1:].reshape(test.shape[0], 1, 28, 28).astype('float32')
    input_shape = (1, img_width, img_height)
else:
    trainX = train[:, 1:].reshape(train.shape[0], 28, 28, 1).astype('float32')
    testX = test[:, 1:].reshape(test.shape[0], 28, 28, 1).astype('float32')
    input_shape = (img_width, img_height, 1)

X_train = trainX / 255.0
y_train = train[:, 0]
# y_train /= 255.0

X_test = testX / 255.0
y_test = test[:, 0]
# y_test /= 255.0

lb = preprocessing.LabelBinarizer()
y_train = lb.fit_transform(y_train)
y_test = lb.fit_transform(y_test)

##############################################

model = Sequential()

# input layer
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# first hidden
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# second hidden
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# third hidden
model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(.2))

# output layer
model.add(Dense(24))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

##############################################

model.summary()

model.fit(
    X_train,
    y_train,
    epochs=epochs,
    batch_size=batch_size
)

score = model.evaluate(X_test, y_test, batch_size=batch_size)

model.save_weights('mnist_try_3.h5')