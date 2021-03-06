import numpy as np
import pandas as pd
import math

def log2(x):
    if x == 0:
        return 0
    return math.log(x,2)

def main():
    file = "training_set2.csv"
    tree = decisionTree()
    testdata =pd.read_csv("test_set2.csv")
    valid = pd.read_csv("validation_set2.csv")
    df = tree.load_csv(file)
    heuristic = 'gain'
    print("building Tree")
    root = tree.buildTree(df,df.columns[:-1], heuristic)
#    depth = 0
    print(tree.parse_tree(root,0))
    print(tree.accuracy(df,root))
    print(tree.accuracy(testdata,root))
    print(tree.accuracy(valid,root))
    
    root2 = tree.buildTree(df,df.columns[:-1],'variance')
    print(tree.parse_tree(root2,0))
#    print(depth)
    print(tree.accuracy(df,root2))
    print(tree.accuracy(testdata,root2))
    print(tree.accuracy(valid,root2))
class Node:
    def __init__(self):
        self.attr = None
        self.value = None
        self.left = None
        self.right = None
        self.parent = None
        
class decisionTree:
    def __init__(self):
        self.dataset = None
    
    def load_csv(self,filename):
        df = pd.read_csv(filename)
        self.dataset = df
        return df
    def getCount(self, arr):
        count = np.unique(arr, return_counts = True)[1]
        return count
                
    def entropy(self,column):
        counts = self.getCount(column)
        entropy = 0.0
        if len(counts)==0:
            return 0.0
        total = sum(counts)
        for i in range(len(counts)):
            entropy += -float(counts[i])/total*np.log2(float(counts[i])/total)
        return entropy
        
        
    def InfoGain_entropy(self,data,attr_name):
        total_entropy = self.entropy(data["Class"])
        counts= self.getCount(data[attr_name])
        
        attr_Entropy = 0.0
        for i in range(len(counts)):
            probability = float(counts[i])/sum(counts)
            split = data.where(data[attr_name]==i).dropna()
            split_entropy = self.entropy(split["Class"])
            attr_Entropy += probability * split_entropy
        
        return total_entropy - attr_Entropy
        
    def variance(self, column):
        counts = self.getCount(column)
        total = sum(counts)
        if len(counts)<=1:
            return 0
        variance = 1
        for i in range(len(counts)):
            variance*= float(counts[i])/total
        return variance
        
    def InfoGain_variance(self,data,attr_name):
        total_variance = self.variance(data["Class"])
        counts= self.getCount(data[attr_name])
        attr_impurity = 0
        for i in range(len(counts)):
            probability = float(counts[i])/sum(counts)
            split = data.where(data[attr_name]==i).dropna()
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
        if len(unique) == 1:
            node.value = int(unique[0])
        
        elif len(data)==0:
            node.value = self.max_freq(self.dataset, "Class")
        
        elif len(attributes) ==0:
            node.value = node.parent
        else:
            node.parent = self.max_freq(data, "Class")
            
            max_gain = np.NINF
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
                    gain = self.InfoGain_variance(data,attr)
                    if max_gain<gain:
                        max_gain = gain
                        best_attr = attr
                        
            node.attr = best_attr
                
            newAttrs = []
            for attr in attributes:
                if attr!=best_attr:
                    newAttrs.append(attr)
            attributes = newAttrs
                
            dataL = data.where(data[best_attr] == 0).dropna()
            print(dataL)
            node.left = self.buildTree(dataL,attributes, heuristic)
                
            dataR = data.where(data[best_attr] == 1).dropna()
            node.right = self.buildTree(dataR,attributes,heuristic)
            
        return(node)
        
    def parse_tree(self, node , depth):
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
            tree = tree + self.parse_tree(node.left, depth + 1)
            tree = tree + sign
        else:
            tree = tree + temp + "=0:\n"
            tree = tree + self.parse_tree(node.left, depth + 1)
            tree = tree + sign

        if node.right.right is None and node.right.left is None:
            tree = tree + temp + "=1:"
            tree = tree + self.parse_tree(node.right, depth + 1)
        else:
            tree = tree + temp + "=1:\n"
            tree = tree + self.parse_tree(node.right, depth + 1)

        return tree

    def evaluate(self,data,value,node):
        if node.attr is None:
            return node.value
        else:
            if data[node.attr][value] == 0:
                return self.evaluate(data, value, node.left)
            else:
                return self.evaluate(data, value, node.right)
    
    def accuracy(self, data, root):
        predict = 0.0
        print(root.value)
        for i in range(len(data["Class"])):
            if self.evaluate(data, i, root) == data["Class"][i]:
                predict+=1
        return float(predict)/len(data["Class"])

    
main()




