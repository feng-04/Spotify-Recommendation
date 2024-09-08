# data storage and visualization

import numpy as np
import matplotlib.pyplot as plt
import csv

attributes = ["danceability", "energy", "loudness", "acousticness", "valence", "tempo"]



class datas:
    def __init__(self):
        pass

    def storingliked(self, spotifyapi):
        csvfile = 'likedsong.csv'
        ids = spotifyapi.get_liked_vectors()
        with open(csvfile, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(attributes)
            writer.writerows(ids)

    def stored_negative(self, spotifyapi):
        csvfile = 'negativeset.csv'
        vectors = spotifyapi.negativeset()
        with open(csvfile, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(attributes)
            writer.writerows(vectors)


    def opening(self, attribute):
        datalist = []
        with open('likedsong.csv', 'r') as file:
            reader = csv.DictReader(file)
            for item in reader:
                # need to convert it to number, or else it is treted as a string
                datalist.append(float(item[attribute]))
        return datalist
    
    def histogram(self, attribute):
        fig, ax = plt.subplots(2,2)
        everything = []
        data = self.opening(attribute)
        for i in range(2):
            for j in range(2):
                ax[i, j].hist(data, bins=(i+j+5)*10, linewidth=0.1)
                ax[i, j].set(xlim= (0, 210), ylim=(0, 80))
        plt.show()
    
    def plotovertime(self, attribute):
        fig, ax = plt.subplots()
        # 0, 1, 2, 3, 4, 5
        data = self.opening(attribute)
        average = self.average_over_time(data)
        ax.plot(data)
        ax.plot(average, color = 'red')
        ax.set_title(f"{attribute}")
        plt.show()

    def plot_compare(self, attribute1, attribute2):
        data1 = self.opening(attribute1)
        data2 = self.opening(attribute2)
        plt.plot(data1, data2)
        plt.show()
    
    def correlation(self, one, two):
         data1  = self.opening(one)
         data2 = self.opening(two)
         return(np.corrcoef(data1, data2))
    

    def average_over_time(self, dataset):
        array = []
        sum = 0
        for i in range(len(dataset)):
            sum += dataset[i]
            average = sum / (i+1)
            array.append(average)
        return array
    

    
