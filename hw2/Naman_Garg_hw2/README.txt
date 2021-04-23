To compile and run:
	python NaiveBayes.py

Example:
ngarg3@remote-n17: hw2 % python NaiveBayes.py
Accuracy Training:  0.9568034557235421
Accuracy Test_with_stopwords:  0.8577405857740585
Accuracy Test_without_stopwords:  0.8661087866108786

The path for reading training and test dataset, /train/ham, /train/spam, /test/spam, /test/ham, the train and test folders should in same folder as the NaiveBayes.py file for the program to run.

I created a text file stopWords.txt which is read by the classifier to filter documents.