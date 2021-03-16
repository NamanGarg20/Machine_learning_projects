import numpy as np
import pandas as pd
import math
from pprint import pprint

dataset = None
def main():
    file = "training_set.csv"
    tree = decisionTree()
    
    df = tree.load_csv(file)
    root = tree.buildTree(df,df.columns[:-1])
    print(tree.print_tree(root,0))
    tree.print_tree2(root,0)
    #test(df,root)
class Node:
    def __init__(self):
        self.attr = None
        self.value = None
        self.left = None
        self.right = None
class decisionTree:
    def __init__(self):
        self.dataset = None
    
    def load_csv(self,filename):
        df = pd.read_csv(filename)
        self.dataset = df
        return df

    def entropy(self,column):
        counts = np.unique(column,return_counts = True)[1]
        entropy = 0
        total =np.sum(counts)
        for i in range(len(counts)):
            entropy += -counts[i]/total*np.log2(counts[i]/total)
        return entropy
        
        
    def InfoGain(self,data,attr_name):
        total_entropy = self.entropy(data["Class"])
        counts= np.unique(data[attr_name],return_counts=True)[1]
        
        attr_Entropy = 0
        for i in range(len(counts)):
            probability = counts[i]/np.sum(counts)
            split = data.where(data[attr_name]==i).dropna()
            split_entropy = self.entropy(split["Class"])
            attr_Entropy += probability * split_entropy
        
        info_gain = total_entropy - attr_Entropy
        return info_gain

    def max_freq(self,data, target):
        counts = np.unique(data[target],return_counts=True)[1]
        freq = np.argmax(counts)
        return int(np.unique(data[target])[freq])

    def buildTree(self, data, attributes, parent = None):
        node = Node()
        unique = np.unique(data["Class"])
        if len(unique) == 1:
            node.value = int(unique[0])
        
        elif len(data)==0:
            node.value = self.max_freq(self.dataset, "Class")
        
        elif len(attributes) ==0:
            node.value = parent
        else:
            parent = self.max_freq(data, "Class")
            info_gains = []
            for attr in attributes:
                info_gains.append(self.InfoGain(data,attr))
                    
            idx = np.argmax(info_gains)
            best_attr = attributes[idx]
                
            node.attr = best_attr
                
            newAttrs = []
            for attr in attributes:
                if attr!=best_attr:
                    newAttrs.append(attr)
            attributes = newAttrs
                
            dataL = data.where(data[best_attr] == 0).dropna()
            node.left = self.buildTree(dataL,attributes,parent)
                
            dataR = data.where(data[best_attr] == 1).dropna()
            node.right = self.buildTree(dataR,attributes,parent)
            
        return(node)
        
#    def buildTree2(self, data, attributes, parent = None):
#        unique = np.unique(data["Class"])
#        if len(unique) == 1:
#            return unique[0]
#
#        elif len(data)==0:
#            return self.max_freq(self.dataset, "Class")
#
#        elif len(attributes) ==0:
#            return parent
#
#        else:
#            parent = self.max_freq(data, "Class")
#            info_gains = []
#            for attr in attributes:
#                info_gains.append(self.InfoGain(data,attr))
#
#            idx = np.argmax(info_gains)
#            best_attr = attributes[idx]
#
#            tree = {best_attr:{}}
#
#            newAttrs = []
#            for attr in attributes:
#                if attr!=best_attr:
#                    newAttrs.append(attr)
#            attributes = newAttrs
#
#            dataL = data.where(data[best_attr] == 0).dropna()
#            left_tree = self.buildTree(dataL,attributes,parent)
#            tree[best_attr][0] = left_tree
#
#            dataR = data.where(data[best_attr] == 1).dropna()
#            right_tree = self.buildTree(dataR,attributes,parent)
#            tree[best_attr][1] = right_tree
#
#        return(tree)

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
            tree += node.attr + "=0:"
            tree += self.print_tree(node.left, depth + 1)
            tree += sign
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

    def predict(query,tree,default = 1):
        for key in list(query.keys()):
            if key in list(tree.keys()):
            
                try:
                    result = tree[key][query[key]]
                except:
                    return default
      
                result = tree[key][query[key]]
                
                if isinstance(result,dict):
                    return predict(query,result)

                else:
                    return result



    def test(data,tree):
        
        queries = data.iloc[:,:-1].to_dict(orient = "records")
        predicted = pd.DataFrame(columns=["predicted"])
        
        for i in range(len(data)):
            predicted.loc[i,"predicted"] = predict(queries[i],tree,1.0)
        print('The prediction accuracy is: ',(np.sum(predicted["predicted"] == data["Class"])/len(data)))
    
main()




