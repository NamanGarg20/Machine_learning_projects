import sys
import csv
import numpy as np
from collections import defaultdict
import math

def log2(x):
    if x == 0:
        return 0
    return math.log(x,2)

class Node:
    def __init__(self):
        self.attr = ''
        self.value = None
        self.left = None
        self.right = None

class DecisionTree:
    def __init__(self):
        self.root = Node()

    def load_csv(self,filename):
        columns = defaultdict(list)
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            headers = next(reader)
            for row in reader:
                for i in range(len(headers)):
                    columns[headers[i]].append(row[i])
        return columns
        
    def entropy_class(self, data):
        target_col = data["Class"]
        elements,counts = np.unique(target_col,return_counts = True)
        entropy = np.sum([(-counts[i]/np.sum(counts))*np.log2(counts[i]/np.sum(counts)) for i in range(len(elements))])
        return entropy
        
#    def attrEntropy(self, data, attr):
#        elements,count = np.unique(data[attr],return_counts = True)
#        entropy = 0
#        for i in elements:
#            probability = count[i] / len(data[attr])
#            entropy += probability * np.log2(probability)
#        return entropy
#
#
        
    def split_attr(self, data,count):
#        target_variables,count = np.unique(data["Class"],return_counts = True) #This gives all '1' and '0'
        ClassAtrr =data["Class"]
        entropy_class = self.entropy_class(data)
        best_attr= ''
        max_gain = np.NINF
        #for attr in data.keys():
        attrEnt1 = 0
        attrEnt2 = 0
        for attr in data.keys():
            if attr!="Class":
                num1 = 0
                num2 = 0
                num3 = 0
                num4 = 0
                entropy = 0
                for i in range(len(data[attr])):
                    if data[attr][i] == '0':
                        if ClassAtrr[i]=='0':
                            num1+=1
                        else:
                            num2+=1
                    else:
                        if ClassAtrr[i]=='0':
                            num3+=1
                        else:
                            num4+=1
                prob0 = count[0]/np.sum(count)
                attrEnt1 = (num1/count[0])*log2(num1/count[0]) + (num2/count[1])*log2(num2/count[1])
                prob1 = count[1]/np.sum(count)
                
                attrEnt2 = (num3/count[0])*log2(num3/count[0]) + (num4/count[1])*log2(num4/count[1])
                
                attrEntropy = prob0*(attrEnt1) + prob1*(attrEnt2)
                Info_gain = entropy_class + attrEntropy
                
                if max_gain<Info_gain:
                    max_gain = Info_gain
                    best_attr = attr
        print(max_gain)
        print(best_attr)
        return best_attr
          
          
    
    def buidTree1(self,data):
        node = Node()
        target_variables,count = np.unique(data["Class"],return_counts = True)
        print(target_variables,count)
        
        if len(count)==1 or len(list(data))-1==0 :
            node.value = target_variables[0]
            return node
            
        if count[0]==0:
            node.value = 1
        elif count[1]==0:
            node.value = 0
        elif count[1]>count[0]:
            node.value = 1
        elif count[0]>count[1]:
            node.value = 0
        
        best_attr = self.split_attr(data,count)
        
        if best_attr== '':
            return node
        
        
        node.attr = best_attr
        dataL = defaultdict(list)
        dataR = defaultdict(list)
        for attr in data.keys():
            for i in range(len(data[attr])):
                if data[best_attr][i]=='0':
                    dataL[attr].append(data[attr][i])
                else:
                    dataR[attr].append(data[attr][i])
        dataL.pop(best_attr)
        dataR.pop(best_attr)
        try:
            node.left= self.buidTree1(dataL)
            node.right= self.buidTree1(dataR)
        except:
            node.left = None
            node.right = None
        return node
    
    def print_tree(self, node, depth):
        tree = ''
        sign = ''
        if node is None:
            return ' '
        if node.left is None and node.right is None:
            tree = tree + str(node.value) + '\n'
            return tree
        for i in range(depth):
            sign = sign + '| '
        tree = tree + sign
        temp = node.attr
        if node.left.left is None and node.left.right is None:
            tree = tree + temp + "=0:"
            tree = tree + self.print_tree(node.left, depth + 1)
            tree = tree + sign
        else:
            tree = tree + temp + "=0:\n"
            tree = tree + self.print_tree(node.left, depth + 1)
            tree = tree + sign

        if node.right.right is None and node.right.left is None:
            tree = tree + temp + "=1:"
            tree = tree + self.print_tree(node.right, depth + 1)
        else:
            tree = tree + temp + "=1:\n"
            tree = tree + self.print_tree(node.right, depth + 1)

        return tree
    def Accuracy(self, root, data):

        accurate_predictions = 0
        for i in range(len(data["Class"])):
            value = data["Class"][i]
            if self.predict(root, data, value) == value:
                accurate_predictions+=1
        print(accurate_predictions)
        print(len(data["Class"]))
        return accurate_predictions/len(data["Class"])
        
    def predict(self, node, data, value):
        if node.attr == '':
            return node.value
        if value == 1:
            return self.predict(node.right, data, value)
        else:
            return self.predict(node.left, data , value)

def main():
    tree1 = DecisionTree()
    tree2 =DecisionTree()
    trainData = tree1.load_csv("training_set.csv")
    testData = tree2.load_csv("test_set.csv")

    treeRoot = tree1.buidTree1(trainData)
    treeRoottest =tree1.buidTree1(testData)
    
    print(tree1.print_tree(treeRoot, 0))
    print(tree1.Accuracy(treeRoot, trainData))
    print(tree2.Accuracy(treeRoottest, testData))
    
        
#print(load_csv("training_set.csv")[0])
main()
