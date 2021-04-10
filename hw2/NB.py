import numpy as np
import sys
import os
from collections import Counter
from collections import defaultdict
from nltk.stem import PorterStemmer
from pprint import pprint
import copy


class MultinomialNaiveBayes:
    def __init__(self):
        
        self.prior_ham = 0
        self.prior_spam = 0
        
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
        num_class = 0
        for filename in os.listdir(path):
            nPath = path + "/" + filename
            file = open(nPath,'r', errors='ignore')
            words = Counter(file.read().split())
            words = self.stemData(words)
            for word, count in words.items():
                if word in data[Class]:
                    data[Class][word] += count
                else:
                    data[Class][word] = count
            num_class += 1
        
#        list_to_remove = list(data[Class].keys())
#        for item in list_to_remove:
#            if item.isalpha() == False:
#                data[Class].pop(item)
#            elif len(item) == 1:
#                data[Class].pop(item)
                        
        return num_class
    
        
    def condProb(self, data, Class, words):
        #conditional Prob = Count(xi=x, y=Y)+1/(sum(Count(xi=x',Y=y)) + 1*n)
        #unique values in data for a Class
        n = len(data[Class].keys())
#        d = {}
#        n = 0 #unique vocabs in the data
#        for i, num in data['ham'].items():
#            d[i]= i
#            n+=1
#        for i, num in data['spam'].items():
#            if i not in d:
#                d[i]=i
#                n+=1
                
        condProb = defaultdict()
        for i in data[Class].keys():
            prob = float(data[Class][i]+1)/(words+ n) # laplace smoothing
            condProb[i] = prob
        return condProb

    def trainMNB(self, stopWords=False):
        data = defaultdict(defaultdict)
        #Load_ham
        nums_ham = self.loadData(data,"ham","./train/ham")
        
        if stopWords:
            self.removeStopWords(data["ham"])
        words_ham = sum(data["ham"].values())
        #print(words_ham)
        #Load_Spam
        nums_spam = self.loadData(data,"spam","./train/spam")
        if stopWords:
            self.removeStopWords(data["spam"])
        words_spam = sum(data["spam"].values())
        
        
        #print(words_spam)
        total_class = nums_spam + nums_ham
        #prior  P(Y=y) = Count(Y=y)/ sum(Count(Y=y'))
        self.prior_ham = float(nums_ham)/total_class
        self.prior_spam = float(nums_spam)/total_class
        
        
        condProb_ham = self.condProb(data, "ham", words_ham)
        condProb_spam = self.condProb(data, "spam", words_spam)
        

        return [condProb_ham, condProb_spam]
        
    def predict(self, data, condProbs):
        condProb_ham, condProb_spam = condProbs
        ham_score = np.log(self.prior_ham)
        spam_score = np.log(self.prior_spam)
        
        for text, count in data.items():
            if text in condProb_ham:
                ham_score += np.log(float(condProb_ham[text]))*count
            if text in condProb_spam:
                spam_score += np.log(float(condProb_spam[text]))*count
        
        if abs(ham_score) > abs(spam_score):
            return "ham"
        else:
            return "spam"
        
    def accuracy(self, condProbs, path, stopWords=False):
        hams = 0
        spams = 0
        total = 0
        path_ham = path + "/ham"
        
        
        for filename in os.listdir(path_ham):
            nPath = path_ham + "/" + filename
            file = open(nPath,'r', errors='ignore')
            words = Counter(file.read().split())
            words = self.stemData(words)
            if stopWords:
                self.removeStopWords(words)
            if self.predict(words, condProbs) == "ham":
                hams+=1
            total+=1
            
        path_spam = path + "/spam"
        for filename in os.listdir(path_spam):
            nPath = path_spam + "/" + filename
            file = open(nPath, 'r', errors='ignore')
            words = Counter(file.read().split())
            words = self.stemData(words)
            if stopWords:
                self.removeStopWords(words)
            if self.predict(words, condProbs) == "spam":
                spams+=1
            total+=1
        return float(spams+hams)/total
                
            

def main():
    NB = MultinomialNaiveBayes()
    condProbs_train = NB.trainMNB()
    #pprint(condProbs_train)
    print("training_accuracy: ", NB.accuracy(condProbs_train, "./train"))
    
    print("test_accuracy: " , NB.accuracy(condProbs_train,"./test"))
    
    condProbs_train_filter = NB.trainMNB(stopWords= True)
    #pprint(condProbs_train_stopWords)
    print("test_accuracy with filter: " , NB.accuracy(condProbs_train_filter,"./test", stopWords=True))
    
    

main()
