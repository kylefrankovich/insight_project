import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import csv
import pandas as pd

csv_output_file = '/Users/kylefrankovich/Desktop/insight_training_data/tattoo_training_image_labels.csv'

# check if we've got a file going:
if os.path.exists(csv_output_file):
    print('appending to existing file')
    myFile = open(csv_output_file, 'a')
    df_to_append_to = pd.read_csv(csv_output_file)
    labeled_image_names = list(df_to_append_to['file_name'])
    myFields = ['file_name', 'category']
    writer = csv.DictWriter(myFile, fieldnames=myFields)
else:
    print('creating new file')
    myFile = open(csv_output_file, 'w')
    myFields = ['file_name', 'category']
    writer = csv.DictWriter(myFile, fieldnames=myFields)
    writer.writeheader()
    labeled_image_names = []

image_dir = '/Users/kylefrankovich/Desktop/insight_training_data'
image_list = []
for dir, subdir, files in os.walk(image_dir):
    for file in files:
        # only read in .jpgs that haven't already been labeled
        if file.endswith('.jpg') and os.path.join(dir, file) not in labeled_image_names:
            image_list.append(os.path.join(dir, file))

category=[]
plt.ion()


with myFile:
    for i,image in enumerate(image_list):
        img=mpimg.imread(image)
        plt.imshow(img)
        plt.pause(0.05)
        print('\n')
        print(image)
        category.append(input('tattoo (1) or no tattoo (0): '))
        writer.writerow({'file_name' : image, 'category': category[i]})
