#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import glob2
from scipy.io import savemat
from topics_table import topics_table

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
#topics = ['living-rooms', 'beds', 'guest-beds', 'bathrooms', 'kitchens', 'child-rooms', 'sofas', 'bedrooms', 'wall-clocks', 'stoves']

topics = list(topics_table.keys())

acc5_list = []
conf_list = []
cent_list = []
category_list = []
price_list = []

for k in range(len(topics)):
    class_name = topics[k]
    topic_idx = topics_table[class_name]
    print('prediction for class : '+class_name)
    file_num = len(glob2.glob(img_path+class_name+'/*.jpg'))
    label_name = img_path + class_name + '/label.txt'
    cat_acc5_list = []
    with open(label_name, 'r') as label:
        for i in range(file_num):
            line = label.readline()
            line_split = line.split('$')[1].split(' ', 2)
            price = int(line_split[0].replace(',', ''))
            price_list.append(price)

    log_name = img_path + class_name + '/log.txt'
    with open(log_name, 'w') as log:
        for i in range(file_num):
            img_name = img_path + class_name + '/' + str(i) + '.jpg'
            img = image.load_img(img_name, target_size=(224, 224))
            x = image.img_to_array(img)
            #x = x/255.
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            preds = model.predict(x)
            decoded = decode_predictions(preds, top=5)[0]
            ind = np.argpartition(np.ndarray.flatten(preds), -5)[-5:]
            if isinstance(topic_idx, int):
                acc5 = np.any(ind == topic_idx)
                conf = preds[0, topic_idx]
            else:
                acc5 = map(lambda x: np.any(ind == x), topic_idx)
                acc5 = min(sum(acc5), 1)
                conf = np.mean(np.fromiter(map(lambda x: preds[0, x], topic_idx), dtype=float))
            category_list.append(k)
            acc5_list.append(acc5)
            conf_list.append(conf)

            log.write('{}.jpg ({}) prediction results\n'.format(i, class_name))
            #print(preds[:, topics_idx[k]])
            for j in range(len(decoded)):
                log.write('  {} {:.4f}\n'.format(decoded[j][1], decoded[j][2]))
savemat('resnet101.mat', mdict={'price': price_list, 'acc5': acc5_list, 'conf': conf_list, 'category':category_list})
plt.scatter(price_list, conf_list)
plt.show()
