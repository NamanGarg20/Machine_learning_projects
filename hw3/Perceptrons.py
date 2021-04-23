import numpy as np
import sys
import os
import io
from collections import Counter
from collections import defaultdict
from nltk.stem import PorterStemmer
from pprint import pprint



class Perceptron:
    def __init__(self, threshold=100, learning_rate=0.1):
        self.weights = {'zero':1.0}
        self.epochs = threshold
        self.learning_rate = learning_rate
        self.stopWords = False
        
    def stemData(self, wordcount):
        stemmer = PorterStemmer()
        words = {stemmer.stem(word):count for word, count in wordcount.items()}
        return words

    def loadStopWords(self, filename):
        stopWords = []
        with open(filename, 'r') as f:
            stopWords = f.read().split()
        return stopWords
            
    def removeStopWords(self, data):
        stopWords = self.loadStopWords('stopWords.txt')
        for i in stopWords:
            if i in data:
                data.pop(i)
    
    def loadData(self, data, Class, path):
        for filename in os.listdir(path):
            nPath = path + "/" + filename
            file = io.open(nPath,'r', errors='ignore')
            words = Counter(file.read().split())
            words = self.stemData(words)
            if self.stopWords:
                self.removeStopWords(words)
            data[Class][filename] = words
                


    def train(self):
        data = defaultdict(defaultdict)

        self.loadData(data,"ham","./train/ham")

        self.loadData(data,"spam","./train/spam")

        return data
        
#
        
    def trainingRule(self):

        data = self.train()

        for i in range(self.epochs):
            for cls in data.keys():
                for file in data[cls].keys():
                    words = data[cls][file]
                    output = self.predict(words)
                    if cls == "ham":
                        target_value = 1
                    else:
                        target_value = -1
                    for word, count in words.items():
                        self.weights[word] += float(self.learning_rate)*float((target_value - output))*float(count)

                
        
    def predict(self, words):
        total = self.weights['zero']
        for word, count in words.items():
            if word not in self.weights:
                self.weights[word] = 0.0
            total += self.weights[word]*count
        if total > 0.0:
            prediction = 1
        else:
            prediction = -1
        return prediction
            
        
    def accuracy(self,path):
        hams = 0
        spams = 0
        total = 0
        
        self.trainingRule()
        
        path_ham = path + "/ham"
        
#        pprint(self.weights)
        
        for filename in os.listdir(path_ham):
            nPath = path_ham + "/" + filename
            file = io.open(nPath,'r', errors='ignore')
            words = Counter(file.read().split())
            words = self.stemData(words)
            if self.stopWords:
                self.removeStopWords(words)
            if self.predict(words) == 1:
                hams+=1
            total+=1
            
        path_spam = path + "/spam"
        for filename in os.listdir(path_spam):
            nPath = path_spam + "/" + filename
            file = io.open(nPath, 'r', errors='ignore')
            words = Counter(file.read().split())
            words = self.stemData(words)
            if self.stopWords:
                self.removeStopWords(words)
            if self.predict(words) == -1:
                spams+=1
            total+=1
        return float(spams+hams)/total
                
            

def main():
    epochs = [10, 50, 100, 500]
    learningRates = [0.01, 0.05, 0.1, 0.5, 0.8]
    
#    print("Accuracy Training: ", perceptron.accuracy( "./train"))
    print("Accuracy on Test with stop Words\n")
    i=0
    for epoch in epochs:
        for lr in learningRates:
            i+=1
            perceptron = Perceptron()
            perceptron.learning_rate = lr
            perceptron.epochs = epoch
            s = str(i)+ " learning rate: "+ str(perceptron.learning_rate)+ " Iterations: "+ str(perceptron.epochs)+" Accuracy: "+ str(perceptron.accuracy("./test"))
            print(s)
    
#    perceptron = Perceptron()
#    perceptron.learning_rate = 0.5
#    perceptron.epochs = 10000
#    print(i, ", learning rate:", perceptron.learning_rate, ", Iterations:", perceptron.epochs, ", Accuracy:" , perceptron.accuracy("./test"))
    
    print("\nAccuracy on Test without stop Words\n")
    i=0
    for epoch in epochs:
        for lr in learningRates:
            i+=1
            perceptron = Perceptron()
            perceptron.learning_rate = lr
            perceptron.epochs = epoch
            perceptron.stopWords = True
            s = str(i)+ " learning rate: "+ str(perceptron.learning_rate)+ " Iterations: "+ str(perceptron.epochs)+" Accuracy: "+ str(perceptron.accuracy("./test"))
            print(s)
#    perceptron = Perceptron()
#    perceptron.learning_rate = 0.5
#    perceptron.epochs = 10000
#    print(i, ", learning rate:", perceptron.learning_rate, ", Iterations:", perceptron.epochs, ", Accuracy:" , perceptron.accuracy("./test"))
    

if __name__ == "__main__":
    main()
