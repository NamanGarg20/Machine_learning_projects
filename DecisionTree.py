import sys
import csv
import numpy as np
from collections import defaultdict

class Node:
    def __init__(self):
        self.attr = None
        self.value = None
        self.left = None
        self.right = None
        self.parent = None

class DecisionTree:
    def __init__(self):
        self.dataset = None

    def load_csv(self,filename):
        columns = defaultdict(list)
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            headers = next(reader)
            for row in reader:
                for i in range(len(headers)):
                    columns[headers[i]].append(row[i])
        if self.dataset is None:
            self.dataset = columns
        return columns
        
    def split_dataset(self, data, best_attr, value):
        newdata = defaultdict(list)
        
        if len(data[best_attr])==0: # for missing data
            return newdata
            
        for attr in data.keys():
            for i in range(len(data[attr])):
                if data[best_attr][i] == value:
                    newdata[attr].append(data[attr][i])
        return newdata
        
    def getCount(self, arr):
        count = np.unique(arr, return_counts = True)[1]
        return count
                
    def entropy(self,column):
        counts = self.getCount(column)
        entropy = 0.0
        total = sum(counts)
        if len(counts)==0:
            return 0.0
        for i in range(len(counts)):
            entropy += -float(counts[i])/total*np.log2(float(counts[i])/total)
        return entropy
        
        
    def InfoGain_entropy(self,data,attr_name):
        total_entropy = self.entropy(data["Class"])
        counts= self.getCount(data[attr_name])
        
        attr_Entropy = 0.0
        for i in range(len(counts)):
            probability = float(counts[i])/sum(counts)
            split = self.split_dataset(data, attr_name, str(i))
            split_entropy = self.entropy(split["Class"])
            attr_Entropy += probability * split_entropy
        
        return total_entropy - attr_Entropy
        
    def variance(self, column):
        counts = self.getCount(column)
        total = sum(counts)
        if len(counts)<=1:
            return 0
        variance = 1.0
        for i in range(len(counts)):
            variance*= float(counts[i])/total
        return variance
        
    def InfoGain_variance(self,data,attr_name):
        total_variance = self.variance(data["Class"])
        counts= self.getCount(data[attr_name])
        attr_impurity = 0.0
        for i in range(len(counts)):
            probability = float(counts[i])/sum(counts)
            split = self.split_dataset(data,attr_name,str(i))
            split_variance = self.variance(split["Class"])
            attr_impurity += probability * split_variance
            
        gain = total_variance - attr_impurity
        return gain

    def max_freq(self,data, target):
        counts = self.getCount(data[target])
        freq = np.argmax(counts)
        return int(np.unique(data[target])[freq])
    
    def buildTree(self, data, attributes, heuristic):
        node = Node()
        unique = np.unique(data["Class"])
        if len(unique) == 1: # return the value if all the values in "Class" attribute are same
            node.value = int(unique[0])
        
        elif len(data["Class"])==0:
            node.value = self.max_freq(self.dataset, "Class")
        
        elif len(attributes) ==0:
            node.value = node.parent
        else:
            node.parent = self.max_freq(data, "Class")
            
            max_gain = np.NINF # -infinity
            best_attr = ''
            if heuristic=='gain':
                for attr in attributes:
                    if attr!="Class":
                        gain = self.InfoGain_entropy(data,attr)
                        if max_gain<gain:
                            max_gain = gain
                            best_attr = attr
            elif heuristic=='variance':
                
                for attr in attributes:
                    if attr!="Class":
                        gain = self.InfoGain_variance(data,attr)
                        if max_gain<gain:
                            max_gain = gain
                            best_attr = attr
                        
                
            node.attr = best_attr
                
            #remove the best attribute from the dataset
            newAttrs = []
            for attr in attributes:
                if attr!=best_attr:
                    newAttrs.append(attr)
            attributes = newAttrs
                
            dataL = self.split_dataset(data, best_attr, '0') #spliting the dataset on the best attribute's values
            node.left = self.buildTree(dataL,attributes, heuristic) #left branch
                
            dataR = self.split_dataset(data, best_attr, '1')
            node.right = self.buildTree(dataR,attributes,heuristic) #right branch
            
        return(node)
        
        
    def parse_tree(self, node , n):
        s = ''
        for i in range(n):
            s+= '| '
            
        #left sub tree
        s+= node.attr +"=0:"
        if node.left.value is not None:
            s+=str(node.left.value)+'\n'
        else:
            s+='\n'
            s+=self.parse_tree(node.left, n+1)
        for i in range(n):
            s+= '| '
            
        #right sub tree
        s+= node.attr +"=1:"
        if node.right.value is not None:
            s+=str(node.right.value)+'\n'
        else:
            s+='\n'
            s+=self.parse_tree(node.right, n+1)
        return s

    def evaluate(self,data,value,node):
        if node.attr is None:
            return node.value
        else:
            if len(data[node.attr])!=0:
                if data[node.attr][value] == '0':
                    return self.evaluate(data, value, node.left)
                else:
                    return self.evaluate(data, value, node.right)
            else:
                return node.value
    
    def accuracy(self, data, root):
        predict = 0.0
        for i in range(len(data["Class"])):
            if self.evaluate(data, i, root) == int(data["Class"][i]):
                predict+=1
        return predict/len(data["Class"])
    
    

def main():
    if (len(sys.argv) < 5): usage();
    training_set = sys.argv[1]
    validation_set = sys.argv[2]
    test_set = sys.argv[3]
    to_print = sys.argv[4]
    heuristic = sys.argv[5]
    
    tree = DecisionTree()
    trainData = tree.load_csv(training_set)
    validationData = tree.load_csv(validation_set)
    testData = tree.load_csv(test_set)
    
    treeRoot = tree.buildTree(trainData, trainData.keys(), heuristic)
    print('Accuracy for '+ heuristic+ ' heuristic for Training: '+ tree.accuracy(trainData, treeRoot) )
    print('Accuracy for '+ heuristic+ ' heuristic for Validation: '+ tree.accuracy(validationData, treeRoot) )
    print('Accuracy for '+ heuristic+ ' heuristic for Testing: '+ tree.accuracy(testData, treeRoot) )
        

    if to_print=='yes':
        print(tree.parse_tree(treeRoot, 0))
    
def usage():
    print('usage: pyhton DecisionTrees.py <training-set> <validation-set> <test-set> <to-print> to-print:{yes,no} <heuristic>')
    sys.exit(1)

if __name__ == "__main__":
    main()
