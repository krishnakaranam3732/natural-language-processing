import os
import re
import ast
import math
from sklearn.feature_extraction.text import CountVectorizer
from scipy import spatial

stringInput = 'strings.txt'
clusterInput = 'cluster3_4.txt'

clusters = {}
clusterString = {}

def getStrings(stringInput):
    vocab = {}
    maxLen = 0
    with open(stringInput,"r+", encoding="latin1") as theFile:
        storeFileData = theFile.readlines()
        for eachLine in storeFileData:
            tokens = eachLine.split()
            if len(tokens) <2:
                tokens.append("")
            strLen = len(tokens[1])
            if strLen > maxLen:
                maxLen = strLen
            vocab[tokens[0]] = tokens[1]
    return [vocab, maxLen]

def getClusters(clusterInput):
    clusters = {}
    with open(clusterInput,"r+", encoding="latin1") as theFile:
        storeFileData = theFile.readlines()
        for eachLine in storeFileData:
            eachLine = re.sub(r"\s\[", "*#*[", eachLine)
            tokens = eachLine.split("*#*")
            print("token is --"+tokens[0]+"--")
            clusters[tokens[0]] = ast.literal_eval(tokens[1])
    return clusters

def addPadding(binaryStr, maxLen):
    strLen = len(binaryStr) 
    strPad = ''
    if strLen < maxLen:
        pad = maxLen - strLen
        strPad = "0" * pad
    return strPad+binaryStr

def convertToVector(binaryStr):
    strList = []
    for each in binaryStr:
        strList.append(int(each))
    return strList

def getDotProduct(oneVector,twoVector):
    dotProd = 0.0
    for i in range(0,len(oneVector)-1):
        dotProd += oneVector[i] * twoVector[i]
    return dotProd

def getMagnitude(oneVector):
    magSum = 0.0
    for i in range(0,len(oneVector)-1):
        magSum += (oneVector[i] * oneVector [i])
    mag = math.sqrt(magSum)
    return mag

def getCosDist(oneVector,twoVector):
    cosDist = 0.0
    dotProd = getDotProduct(oneVector,twoVector)
    magOne = getMagnitude(oneVector)
    magTwo = getMagnitude(twoVector)
    if magOne != 0 and magTwo != 0:
        denominator = magOne * magTwo
        sim = dotProd/denominator
        cosDist = 1-sim
    return cosDist

# get words and binary strings
getString = getStrings(stringInput)

#print("got Strings")

# vocabulary dictionary containing binary strings.
vocabulary = getString[0]
maxLength = getString[1]

#print(vocabulary)
#print(maxLength)

for key in vocabulary:
    strBinary = addPadding(vocabulary[key], maxLength)
    vocabulary[key] = convertToVector(strBinary)

#print("got Vocabulary")

clusters = getClusters(clusterInput)

#print("got Clusters")
clusterOutput = "output3_4.txt"
with open(clusterOutput,"w", encoding="latin1") as theFile:
    for key in clusters:
        totCosDist = 0.0
    #print("start for key: ",key)
        for one in clusters[key]:
            for two in clusters[key]:
                if one != two:
                    oneVector = vocabulary[one]
                    twoVector = vocabulary[two]
                    cDist = getCosDist(oneVector,twoVector)
                    totCosDist += cDist
                    #print(totCosDist)
        avgCosDist = float(totCosDist/len(clusters[key]))
        print("Avg cosine Distance of the cluster "+str(key)+" is :"+str(avgCosDist))
        theFile.write("Avg cosine Distance of the cluster "+str(key)+" is :"+str(avgCosDist)+"\n")

