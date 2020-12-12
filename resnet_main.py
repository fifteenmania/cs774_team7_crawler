# -*- coding: utf-8 -*-

#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import glob2

#from PIL.Image import core as image
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet import preprocess_input, decode_predictions

model = keras.applications.ResNet101(
    include_top = True, weights='imagenet', pooling=max
)

def label_to_data(line):
    return 

# load images
# images 360*360 -> 224, 224
img_path = 'img/'
topics = ['living-rooms', 'beds', 'guest-beds', 'bathrooms', 'kitchens', 'child-rooms', 'sofas', 'bedrooms', 'wall-clocks', 'stoves']

for class_name in topics:
    print('prediction for class : '+class_name)
    with open(img_path+class_name+'/label.txt', 'r') as label:
        file_num = len(glob2.glob(img_path+class_name+'/*.jpg'))
        for i in range(file_num):
            img_name = img_path + class_name + '/' + str(i) + '.jpg'
            img = image.load_img(img_name, target_size=(224, 224))
            x = image.img_to_array(img)
            #x = x/255.
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            preds = model.predict(x)
            decoded = decode_predictions(preds, top=5)[0]
            print('{}.jpg ({}) prediction results'.format(i, class_name))
            print(decoded)
