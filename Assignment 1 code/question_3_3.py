import re
import os
import math

directory = "gutenberg"
fileEncoding = "latin1"

def cleanFile(filePath, fileEncoding):
    with open(filePath,"r+", encoding=fileEncoding) as theFile:
        storeFileData = theFile.readlines()
        theFile.seek(0)
        theFile.truncate()
        for eachLine in storeFileData:
            eachLine = re.sub(r"\r\n+", " ", eachLine)
            eachLine = re.sub(r"\s+", " ", eachLine)
            theFile.write(eachLine)
    
    with open(filePath ,"r+", encoding=fileEncoding) as theFile:
    	storeFileData = theFile.readlines()
    	theFile.seek(0)
    	theFile.truncate()
    	for eachLine in storeFileData:
    		eachLine = re.sub(r"\s+", " ",eachLine)
    		theFile.write(eachLine)

def cleanAllFiles(directory):
    for eachFile in os.listdir(directory):
        fileEncoding = "latin1"
        if eachFile.endswith(".txt"):
            cleanFile(directory+"/"+eachFile, fileEncoding)

def getFileData(filePath, fileEncoding):
    with open(filePath,"r", encoding=fileEncoding) as theFile:
        storeFileData = theFile.readlines()
        return storeFileData

def getAllFiles(directory):
    allFileData = ''
    for eachFile in os.listdir(directory):
        fileEncoding = "latin1"
        if eachFile.endswith(".txt"):
            fileData = getFileData(directory+"/"+eachFile, fileEncoding)
            fileData = str(fileData)
            allFileData = allFileData + fileData
    return allFileData

def getAllFilesData(directory):
    cleanAllFiles(directory)
    return getAllFiles(directory)

def countNgrams(data, ngram):
    nGramDictionary = {}
    
    for i in range (0 ,len(data)-ngram):
        if data[i:i+ngram] in nGramDictionary:
            nGramDictionary[data[i:i+ngram]] += 1
        else:
            nGramDictionary[data[i:i+ngram]] = 1
    
    return nGramDictionary

data = getAllFilesData(directory)
fourGramDictionary = countNgrams(data, 4)
fiveGramDictionary = countNgrams(data, 5)

vocabulary = len(countNgrams(data, 1))

def calculateProbability(fiveGram, fourGram, fiveGramDictionary, fourGramDictionary):
    if fiveGram in fiveGramDictionary: 
        if fourGram in fourGramDictionary:
            probability = float(fiveGramDictionary[fiveGram] + 0.1)/float(fourGramDictionary[fourGram] + (0.1 * vocabulary))
        else:
            probability = float(fiveGramDictionary[fiveGram] + 0.1)/float((0.1 * vocabulary))
    else:
        if fourGram in fourGramDictionary:
            probability = 0.1/float(fourGramDictionary[fourGram] + (0.1 * vocabulary))
        else:
            probability = 0.1/ (0.1 * vocabulary)
    return probability

def calculatePerplexity(testFilePath, fiveGramDictionary, fourGramDictionary):
    cleanFile(testFilePath, fileEncoding)

    with open(testFilePath ,"r+", encoding="latin1") as testFile:
        data = testFile.read()
        totalProbability = 0.0
        for i in range (0 ,len(data)-5):
            totalProbability += math.log(calculateProbability(data[i:i+5], data[i:i+4], fiveGramDictionary, fourGramDictionary), 2)
        fraction = float(-1/len(data))
        logFunction = float(fraction * totalProbability)

    finalPerplexity = math.pow(2, logFunction)
    printPerplexity = 'The perplexity of the file {0} is {1}\n'.format(testFilePath, finalPerplexity)
    print(printPerplexity)

def testAllFiles(testDirectory, fiveGramDictionary, fourGramDictionary):
    for eachFile in os.listdir(testDirectory):
        fileEncoding = "latin1"
        if eachFile.endswith(".txt"):
            calculatePerplexity(testDirectory+"/"+eachFile, fiveGramDictionary, fourGramDictionary)

testAllFiles("SOC", fiveGramDictionary, fourGramDictionary)
