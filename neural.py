import tensorflow as tf
from sklearn.model_selection import train_test_split
import csv
import numpy as np
import sys

TEST_SIZE = 0.3
EPOCHS = 20

def load_data(positive):
    songs = []
    label = []
    if positive:
        filename = 'likedsong.csv'
    else:
        filename = 'negativeset.csv'
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for line in reader:
            singleline = []
            for digit in line:
                digit = float(digit)
                singleline.append(digit)
            songs.append(singleline)
            if positive:
                label.append(1)
            else:
                label.append(0)
    return(songs, label)

def get_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(1024, activation='relu', input_shape=(6,)), 

        tf.keras.layers.Dense(512, activation='relu'),

        tf.keras.layers.Dense(256, activation='relu'),

        tf.keras.layers.Dense(128, activation='relu'),
        
        tf.keras.layers.Dropout(0.3), 

        tf.keras.layers.Dense(1, activation='sigmoid')
    ])


    model.compile(
        optimizer='adam', 
        loss='binary_crossentropy', 
        metrics=['accuracy'])
    return model

def main():
    # load data
    songs = []
    labels = []
    good, label1 = load_data(True)
    bad, label2 = load_data(False)
    songs.extend(good)
    songs.extend(bad)
    labels.extend(label1)
    labels.extend(label2)
    labels = np.array(labels).flatten()

    x_train, x_test, y_train, y_test = train_test_split(
        np.array(songs), labels, test_size=TEST_SIZE
    )
    
    model = get_model()
    model.fit(x_train, y_train, epochs=EPOCHS)
    model.evaluate(x_test, y_test, verbose=2)


    # if the user decides to store the model
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        model.save(filename)


main()

