# -*- coding: utf-8 -*-
"""COVID-19 Multi Class Classification using Convolutional Neural Networks & Transfer Learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uu8D_r2jAKBY2YgjwLfD5Lvftp5_Llht

##### <b>Step-1: Importing Libraries</b>
"""

import os                               
import cv2
import time                              
import numpy as np   
import tensorflow as tf 
from PIL import Image
import numpy as np
from skimage import transform
from google.colab import drive 
from keras import backend as K           
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
from keras.models import load_model
from keras.preprocessing import image  
from keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator

"""##### <b>Step-2: Mounting Drive</b>"""

drive.mount('/content/drive',force_remount=True)

"""##### <b>Step-3: Setting path for Testing, Training and validation directories</b>"""

base_dir = '/content/drive/MyDrive/COVID-19 Deep Learning'
train_dir = '/content/drive/MyDrive/COVID-19 Deep Learning/Train'
validations_dir = '/content/drive/MyDrive/COVID-19 Deep Learning/Validation'
test_dir = '/content/drive/MyDrive/COVID-19 Deep Learning/Test'

"""##### <b>Step-4: Setting path for classes</b>"""

train_covid_dir = '/content/drive/MyDrive/COVID-19 Deep Learning/Train/COVID-19'
train_normal_dir = '/content/drive/MyDrive/COVID-19 Deep Learning/Train/NORMAL'
train_viralpn_dir = '/content/drive/MyDrive/COVID-19 Deep Learning/Train/Viral Pneumonia'

validation_covid_dir = '/content/drive/MyDrive/COVID-19 Deep Learning/Validation/COVID-19'
validation_normal_dir = '/content/drive/MyDrive/COVID-19 Deep Learning/Validation/NORMAL'
validation_viralpn_dir = '/content/drive/MyDrive/COVID-19 Deep Learning/Validation/Viral Pneumonia'

test_covid_dir = '/content/drive/MyDrive/COVID-19 Deep Learning/Test/COVID-19'
test_normal_dir = '/content/drive/MyDrive/COVID-19 Deep Learning/Test/NORMAL'
test_viralpn_dir = '/content/drive/MyDrive/COVID-19 Deep Learning/Test/Viral Pneumonia'

num_covid_train = len(os.listdir(train_covid_dir))
num_normal_train = len(os.listdir(train_normal_dir))
num_viralpn_train = len(os.listdir(train_viralpn_dir))

num_covid_validaition = len(os.listdir(validation_covid_dir))
num_normal_validation= len(os.listdir(validation_normal_dir))
num_viralpn_validation= len(os.listdir(validation_viralpn_dir))

num_covid_test = len(os.listdir(test_covid_dir))
num_normal_test= len(os.listdir(test_normal_dir))
num_viralpn_test= len(os.listdir(test_viralpn_dir))

"""##### <b>Step-5: Printing Total Images of each class</b>"""

print("Total Training COVID Images",num_covid_train)
print("Total Training NORMAL Images",num_normal_train)
print("Total Training VIRALPN Images",num_viralpn_train)

print("--")
print("Total validation COVID Images",num_covid_validaition)
print("Total validation NORMAL Images",num_normal_validation)
print("Total validation VIRALPN Images",num_viralpn_validation)

print("--")
print("Total Test COVID Images", num_covid_test)
print("Total Test NORMAL Images",num_normal_test)
print("Total Test VIRALPN Images",num_viralpn_test)

"""##### <b>Step-6: Printing Total training, testing and validation images</b>"""

total_train = num_covid_train+num_normal_train+num_viralpn_train
total_validation = num_covid_validaition+num_normal_validation+num_viralpn_validation
total_test = num_covid_test+num_normal_test+num_viralpn_test
print("Total Training Images",total_train)
print("--")
print("Total Validation Images",total_validation)
print("--")
print("Total Testing Images",total_test)

"""##### <b>Step-7: Defining Image shape and batch size for Convolutional neural networks</b>"""

IMG_SHAPE  = 150 
batch_size = 50

"""#####<b>Step-8: Function for visualization of images</b>"""

def plotImages(images_arr):
    fig, axes = plt.subplots(1, 5, figsize=(20,20))
    axes = axes.flatten()
    for img, ax in zip(images_arr, axes):
        ax.imshow(img)
    plt.tight_layout()
    plt.show()

"""#####<b>Step-9:Applying Data Augmentation on training data</b>"""

image_gen_train = ImageDataGenerator(rescale = 1./255,rotation_range = 40,width_shift_range=0.2,height_shift_range=0.2,shear_range = 0.2,
                                     zoom_range = 0.2,horizontal_flip = True,fill_mode = 'nearest')
train_data_gen = image_gen_train.flow_from_directory(batch_size = batch_size,
                                                     directory = train_dir,
                                                     shuffle= True,
                                                     target_size = (IMG_SHAPE,IMG_SHAPE),
                                                    class_mode  = "categorical")

"""##### <b>Step-10: showing augmented images</b>"""

augmented_images = [train_data_gen[0][0][0] for i in range(20)]
plotImages(augmented_images)

"""##### <b>Step-11: Preprocessing of validation and testing data</b>"""

image_generator_validation = ImageDataGenerator(rescale=1./255)

val_data_gen = image_generator_validation.flow_from_directory(batch_size=50,
                                                 directory=validations_dir,
                                                 target_size=(IMG_SHAPE, IMG_SHAPE),
                                                 class_mode='categorical')

image_gen_test = ImageDataGenerator(rescale=1./255)

test_data_gen = image_gen_test.flow_from_directory(batch_size=50,
                                                 directory=test_dir,
                                                 target_size=(IMG_SHAPE, IMG_SHAPE),
                                                 class_mode='categorical')

"""##### <b>Step-12: building Convolutional Neural Networks</b>"""

classifier = tf.keras.Sequential([
        tf.keras.layers.Conv2D(16,(3,3),activation='relu',input_shape=(IMG_SHAPE, IMG_SHAPE, 3)),
        tf.keras.layers.MaxPooling2D(2,2),

        tf.keras.layers.Conv2D(32,(3,3),activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),

        tf.keras.layers.Conv2D(64,(3,3),activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        
        tf.keras.layers.Conv2D(128,(3,3),activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),

        tf.keras.layers.Dropout(0.32),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(1024,activation= 'relu'),
        tf.keras.layers.Dense(3, activation = "softmax")  
])

"""##### <b>Step-13: Compiling Convolutional neural networks</b>"""

#classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy',tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])
classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

"""#####<b>Step-14: Printing Model Parameters</b>"""

classifier.summary()

"""#####<b>Step-15: Training the Convolutional Neural Networks</b>"""

history = classifier.fit(train_data_gen,steps_per_epoch=28,epochs = 50,validation_data=val_data_gen,validation_steps=11,verbose = 1)

"""#####<b>Step-16:Checking keys of history variable</b>"""

history_dict = history.history
print(history_dict.keys())

"""#####<b>Step-17:Visualizing the training and validation using accuracy and loss </b>"""

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(50)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

"""#####<b>Step-18:Visualizing the training and validation using accuracy and loss in single graph </b>"""

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(50)

plt.figure(figsize=(8, 8))
plt.subplot(1, 1, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='lower left')
plt.title('Accuracy & Loss')
plt.show()

"""#####<b>Step-19:Saving model in json and h5 format</b>"""

model_json = classifier.to_json()
with open("/content/drive/MyDrive/COVID-19 Deep Learning/COVID_19_Classifier.json", "w") as json_file:
    json_file.write(model_json)
classifier.save('/content/drive/MyDrive/COVID-19 Deep Learning/COVID_19_Classifier.h5')

"""##### <b>Step-20: Testing Model on test data</b>"""

results = classifier.evaluate(test_data_gen,batch_size=50)
print("test_loss, test accuracy",results)

"""#####<b>Step-21:visualizing results with confidence</b>"""

image_1 = cv2.imread('/content/drive/MyDrive/COVID-19 Deep Learning/Test/NORMAL/NORMAL (1095).png')
image = cv2.resize(image_1, (150, 150))
image = image.astype("float")/255.0
image = img_to_array(image)
image = np.expand_dims(image, axis=0)
predict = classifier.predict(image)
classes=np.argmax(predict,axis=1)
if classes==0:
  res = "COVID-19"
elif classes==1:
  res = "NORMAL"
elif classes==2:
  res = "VIRAL PNEUMONIA"
confidence = str(round(max(predict[0]), 2))
plt.imshow(image_1)
print("The below image is ",res," with ",confidence," confidence")

"""###### <b>Step-22: buliding a VGG-16 Model</b>"""

pre_trained_model = tf.keras.applications.VGG16(input_shape=(224, 224, 3), include_top=False, weights="imagenet")
for layer in pre_trained_model.layers:
    print(layer.name)
    layer.trainable = False
    
print(len(pre_trained_model.layers))
last_layer = pre_trained_model.get_layer('block5_pool')
print('last layer output shape:', last_layer.output_shape)
last_output = last_layer.output

x = tf.keras.layers.GlobalMaxPooling2D()(last_output)
x = tf.keras.layers.Dense(512, activation='relu')(x)
x = tf.keras.layers.Dropout(0.5)(x)
x = tf.keras.layers.Dense(3, activation='softmax')(x)

"""#####<b>Step-24:Compiling VGG-16 Model</b>"""

model = tf.keras.Model(pre_trained_model.input, x)
optimizer = tf.keras.optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=True)
model.compile(loss='categorical_crossentropy',optimizer=optimizer,metrics=['accuracy'])

"""#####<b>Step-25:Printing Summary of VGG-16 Model</b>"""

model.summary()

"""#####<b>Step-26:Training VGG-16 Model without Fine Tuning</b>"""

epochs = 3
model_history = model.fit(train_data_gen,epochs = epochs, validation_data = val_data_gen,verbose = 1, steps_per_epoch=28, validation_steps=11)

"""######<b>Step-28:Training VGG-16 Model with Fine Tuning</b>"""

for layer in model.layers[:15]:
    layer.trainable = False

for layer in model.layers[15:]:
    layer.trainable = True

"""##### <b>Step-29:Compiling VGG-16 Model</b>"""

optimizer = tf.keras.optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
model.compile(loss='categorical_crossentropy',optimizer=optimizer,metrics=['acc'])

"""#####<b>Step-30:Printing VGG-16 Model Summary</b>"""

model.summary()

"""##### <b>Step-31:setting the last convolutional block to trainable, we are now retraining for half of the hyperparameters</b>"""

learning_rate_reduction = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_acc', patience=3, verbose=1, factor=0.5, 
                                            min_lr=0.000001, cooldown=3)

"""#####<b>Step-32:Training VGG-16 Model with Fine Tuning</b>"""

epochs = 30
history_mod = model.fit(train_data_gen,epochs = epochs, validation_data = val_data_gen,verbose = 1, steps_per_epoch=28,
                              validation_steps=11, callbacks=[learning_rate_reduction])

"""#####<b>Step-33:Visualizing the training and validation using accuracy and loss in single graph </b>"""

acc = history_mod.history['acc']
val_acc = history_mod.history['val_acc']

loss = history_mod.history['loss']
val_loss = history_mod.history['val_loss']

epochs_range = range(30)

plt.figure(figsize=(8, 8))
plt.subplot(1, 1, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='lower left')
plt.title('Accuracy & Loss')
plt.show()

"""#####<b>Step-34:Saving VGG-16 model in json and h5 format</b>"""

model_json = model.to_json()
with open("/content/drive/MyDrive/COVID-19 Deep Learning/COVID_19_VGG-16_Classifier.json", "w") as json_file:
    json_file.write(model_json)
model.save('/content/drive/MyDrive/COVID-19 Deep Learning/COVID_19_VGG-16-Classifier.h5')

"""######<b>Step-35: Testing VGG-16 Model on Test Data</b>"""

results = model.evaluate(test_data_gen,batch_size=50)
print("test_loss, test accuracy",results)

"""##### <b>Step-36: Visualizing Result of VGG-16 Model with Confidence</b>"""

model = tf.keras.models.load_model('/content/drive/MyDrive/COVID-19 Deep Learning/COVID_19_VGG-16-Classifier.h5')
image_1 = cv2.imread('/content/drive/MyDrive/COVID-19 Deep Learning/Test/NORMAL/NORMAL (1096).png')
heatmap_img = cv2.applyColorMap(image_1, cv2.COLORMAP_JET)
image = cv2.resize(image_1, (224,224))
image = image.astype("float")/255.0
image = img_to_array(image)
image = np.expand_dims(image, axis=0)
predict = model.predict(image)
classes=np.argmax(predict,axis=1)
if classes==0:
  res = "COVID-19"
elif classes==1:
  res = "NORMAL"
elif classes==2:
  res = "VIRAL PNEUMONIA"
confidence = str(round(max(predict[0]), 2))

plt.figure(figsize=(10,10))
f, axarr = plt.subplots(1,2) 
axarr[0].imshow(image_1)
axarr[0].axis("off")
axarr[1].imshow(heatmap_img)
axarr[1].axis("off")
print('Model has {} confidence,that image is of {} class.'.format(confidence,res))

image_2 = cv2.imread('/content/drive/MyDrive/COVID-19 Deep Learning/Test/COVID-19/COVID-19 (1002).png')
heatmap_img = cv2.applyColorMap(image_2, cv2.COLORMAP_JET)
image = cv2.resize(image_2, (224,224))
image = image.astype("float")/255.0
image = img_to_array(image)
image = np.expand_dims(image, axis=0)
predict = model.predict(image)
classes=np.argmax(predict,axis=1)
if classes==0:
  res = "COVID-19"
elif classes==1:
  res = "NORMAL"
elif classes==2:
  res = "VIRAL PNEUMONIA"
confidence = str(round(max(predict[0]), 2))
plt.figure(figsize=(10,10))
f, axarr = plt.subplots(1,2) 
axarr[0].imshow(image_2)
axarr[0].axis("off")
axarr[1].imshow(heatmap_img)
axarr[1].axis("off")
print('Model has {} confidence,that image is of {} class.'.format(confidence,res))

covid_image = cv2.imread('/content/drive/MyDrive/COVID-19 Deep Learning/Test/COVID-19/COVID-19 (1002).png')
covid_image_1 = cv2.imread('/content/drive/MyDrive/COVID-19 Deep Learning/Test/COVID-19/COVID-19 (1005).png')
normal_image = cv2.imread('/content/drive/MyDrive/COVID-19 Deep Learning/Test/NORMAL/NORMAL (1092).png')
normal_image_2 = cv2.imread('/content/drive/MyDrive/COVID-19 Deep Learning/Test/NORMAL/NORMAL (1096).png')
pn_image = cv2.imread('/content/drive/MyDrive/COVID-19 Deep Learning/Test/Viral Pneumonia/Viral Pneumonia (289).png')
pn_image_2 = cv2.imread('/content/drive/MyDrive/COVID-19 Deep Learning/Test/Viral Pneumonia/Viral Pneumonia (292).png')
fig, axarr = plt.subplots(1, 6, figsize=(20,20))
axarr[0].imshow(covid_image)
axarr[0].axis("off")
axarr[1].imshow(normal_image)
axarr[1].axis("off")
axarr[2].imshow(covid_image_1)
axarr[2].axis("off")
axarr[3].imshow(normal_image_2)
axarr[3].axis("off")
axarr[4].imshow(pn_image)
axarr[4].axis("off")
axarr[5].imshow(pn_image_2)
axarr[5].axis("off")
plt.show()