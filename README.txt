to run and compile:
    
    #for gain heuristic and no to print
    python DecisionTree.py training_set.csv validation_set.csv test_set.csv no gain
    
    #for gain heuristic and yes to print
    python DecisionTree.py training_set.csv validation_set.csv test_set.csv yes gain
    
    
    #for gain heuristic and no to print
    python DecisionTree.py training_set.csv validation_set.csv test_set.csv no variance
    
    #for gain heuristic and yes to print
    python DecisionTree.py training_set.csv validation_set.csv test_set.csv yes variance
    
    

In the project to handle missing data, I ignore the instance having missing data and return empty dataset on spilt if missing data is encountered.
    
