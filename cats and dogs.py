# https://www.microsoft.com/en-us/download/confirmation.aspx?id=54765
# down log cats and dogs pictures
import os
import zipfile
import random
import tensorflow as tf
import shutil
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from shutil import copyfile

print(len(os.listdir('D:\\python project\\tensorflow cat and dog\\PetImages\\Cat')))
print(len(os.listdir('D:\\python project\\tensorflow cat and dog\\PetImages\\Dog')))

try:
	os.mkdir('D:\\python project\\tensorflow cat and dog\\cats-v-dogs')
	os.mkdir('D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\training')
	os.mkdir('D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\testing')
	os.mkdir('D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\training\\cats')
	os.mkdir('D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\training\\dogs')
	os.mkdir('D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\testing\\cats')
	os.mkdir('D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\testing\\dogs')
except OSError:
	pass

def split_data(SOURCE,TRAINING,TESTING,SPLIT_SIZE):
	files=[]
	for filename in os.listdir(SOURCE):
		file = SOURCE + filename
		if os.path.getsize(file) > 0:
			files.append(filename)
		else:
			print(filename+"is zero length,so ignoring.")

		training_length = int(len(files) * SPLIT_SIZE)
		testing_length = int(len(files) - training_length)
		shuffled_set = random.sample(files,len(files))
		training_set = shuffled_set[0:training_length]
		testing_set = shuffled_set[-testing_length:]

	for filename in training_set:
		this_file = SOURCE + filename
		destination = TRAINING +filename
		copyfile(this_file,destination)

	for filename in testing_set:
		this_file = SOURCE + filename
		destination = TESTING +filename
		copyfile(this_file,destination)

CAT_SOURCE_DIR = 'D:\\python project\\tensorflow cat and dog\\PetImages\\Cat\\'
TRAINING_CATS_DIR = 'D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\training\\cats\\'
TESTING_CATS_DIR = 'D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\testing\\cats\\'
DOG_SOURCE_DIR = 'D:\\python project\\tensorflow cat and dog\\PetImages\\Dog\\'
TRAINING_DOGS_DIR = 'D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\training\\dogs\\'
TESTING_DOGS_DIR = 'D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\testing\\dogs\\'

def create_dir(file_dir):
	if os.path.exists(file_dir):
		print('true')
		shutil.rmtree(file_dir)
		os.makedirs(file_dir)
	else:
		os.makedirs(file_dir)

create_dir(TRAINING_CATS_DIR)
create_dir(TESTING_CATS_DIR)
create_dir(TRAINING_DOGS_DIR)
create_dir(TESTING_DOGS_DIR)

split_size = .9
split_data(CAT_SOURCE_DIR,TRAINING_CATS_DIR,TESTING_CATS_DIR,split_size)
split_data(DOG_SOURCE_DIR,TRAINING_DOGS_DIR,TESTING_DOGS_DIR,split_size)

print(len(os.listdir('D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\training\\cats')))
print(len(os.listdir('D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\testing\\cats')))
print(len(os.listdir('D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\training\\dogs')))
print(len(os.listdir('D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\testing\\dogs')))


model = tf.keras.models.Sequential([
		tf.keras.layers.Conv2D(16,(3,3),activation='relu',input_shape=(150,150,3)),
		tf.keras.layers.MaxPool2D(2,2),
		tf.keras.layers.Conv2D(32,(3,3),activation='relu'),
		tf.keras.layers.MaxPool2D(2,2),
		tf.keras.layers.Conv2D(64,(3,3),activation='relu'),
		tf.keras.layers.MaxPool2D(2,2),
		tf.keras.layers.Flatten(),
		tf.keras.layers.Dense(512,activation='relu'),
		tf.keras.layers.Dense(1,activation='sigmoid')
])

model.compile(optimizer=RMSprop(lr=0.001),loss='binary_crossentropy',metrics=['acc'])

# ����Ԥ����
TRAINING_DIR = 'D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\training'
train_datagen = ImageDataGenerator(rescale=1.0/255.)
train_generator = train_datagen.flow_from_directory(TRAINING_DIR,batch_size=100,class_mode='binary',target_size=(150,150))

VALIDATION_DIR = 'D:\\python project\\tensorflow cat and dog\\cats-v-dogs\\testing'
validation_datagen = ImageDataGenerator(rescale=1.0/255.)
validation_generator = validation_datagen.flow_from_directory(VALIDATION_DIR,batch_size=100,class_mode='binary',target_size=(150,150))


history = model.fit_generator(train_generator,
							  epochs=6,
							  verbose=1,
							  validation_data=validation_generator)

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs,acc,'r',"Training Accuracy")
plt.plot(epochs,val_acc,'b',"Validation Accuracy")
plt.title('Training and validation accuracy')
plt.figure()
# plt.show()

plt.plot(epochs,loss,'r',"Training Loss")
plt.plot(epochs,val_loss,'b',"Validation Loss")
plt.figure()
plt.show()

# ʹ��ģ��
# import numpy as np
# from google.colab import files
# from tensorflow.keras.preprocessing import image
#
# uploaded = files.upload()
#
# for fn in uploaded.key():
# 	path = '/content/' + fn
# 	img = img.load_img(path,target_size=(150,150)) #�б�
# 	x = image.img_to_array(img) #����
# 	x = np.expand_dim(x,axis=0) #����
#
# 	images = np.vstack([x]) #3��ͨ�����������γ�һ��������
# 	classes = model.predict(images,batch_size=10)
# 	print(classes[0])
# 	if classes[0] >0.5:
# 		print(fn + "is a dog")
# 	else:
# 		print(fn + "is a cat")



# go
