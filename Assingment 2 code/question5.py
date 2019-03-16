# question 5
import re
import os
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV, train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.externals import joblib
from sklearn.metrics import precision_score, recall_score

trainFile = 'train_english_spam.txt'
testFile = 'test_data_english_spam.txt'
modelFile = 'mlp_question5.pkl'
outputFile = 'labels.txt'

def getTrainData(trainFile):
    sentenceList = []
    with open(trainFile,"r+", encoding="latin1") as theFile:
        storeFileData = theFile.readlines()
        for eachLine in storeFileData:
            eachLine = re.sub(r'\n', '', eachLine)
            sentenceList += [eachLine]
    return sentenceList

def printOutput(outputArray):
    with open(outputFile,"w", encoding="latin1") as theFile:
        for each in outputArray:
            if each == 0:
                theFile.write("ham"+"\n")
            else:
                theFile.write("spam"+"\n")

trainLines = []
trainClass = []
trainData = getTrainData(trainFile)
testData = getTrainData(testFile)

for each in trainData:
    data = each.split()
    end = data[len(data)-1]
    lastData = end.split(',')
    data = data[0:len(data)-1]
    data += [lastData[0]]
    each = ''
    for listData in data:
        each += listData + " "
    trainLines.append(each)
    if lastData[1] == 'spam':
        trainClass.append(1)
    else:
        trainClass.append(0)

vectorizer = CountVectorizer()
transformer = TfidfTransformer()

train_counts = vectorizer.fit_transform(trainLines)
trainLinesNP = transformer.fit_transform(train_counts)

trainClassNP = np.asarray(trainClass)

X_train, X_test, y_train, y_test = train_test_split(trainLinesNP, trainClassNP, test_size=0.1, random_state=42)


test_counts = vectorizer.transform(testData)
testLinesNP = transformer.transform(test_counts)

# Multilayer Perceptron to be initialized. 
if __name__ == '__main__':
    if os.path.isfile(modelFile):
        loadModel = joblib.load(modelFile)
        model = loadModel.best_estimator_
        print("model saved as "+modelFile+" is used.")
        testOutput = model.predict(X_test)
        print("recall score for the model is :",recall_score(y_test, testOutput, average='macro'))
        print("precision score for the model is :",precision_score(y_test, testOutput, average='macro'))
        outputArray = model.predict(testLinesNP)
        printOutput(outputArray)
    else:
        parameters = {'activation':['identity'],'hidden_layer_sizes': [(5,1),(10,1)]}
        mlpClassify = MLPClassifier(verbose=10)
        model = GridSearchCV(mlpClassify, parameters, n_jobs=-1, cv=10)
        model.fit(X_train, y_train)
        joblib.dump(model, modelFile)
        testOutput = model.predict(X_test)
        print("recall score for the model is :",recall_score(y_test, testOutput, average='macro'))
        print("precision score for the model is :",precision_score(y_test, testOutput, average='macro'))
        outputArray = model.predict(testLinesNP)
        printOutput(outputArray)
        print("The most useful parameters are: ", model.best_params_)
