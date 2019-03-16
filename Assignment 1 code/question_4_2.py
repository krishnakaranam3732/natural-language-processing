import re
import os

fileEncoding = "latin1"

def processLine(eachLine):
    wordTagList = []
    if eachLine is not "\n":
        eachLine = '<sentence>/<sentence> ' + eachLine + ' <EOS>/<EOS>'
        wordTagList = eachLine.split()
    return wordTagList

def processFile(eachFile):
    with open(eachFile,"r+", encoding=fileEncoding) as theFile:
            storeFileData = theFile.readlines()
            wordTagList = []
            for eachLine in storeFileData:
                eachLineList= processLine(eachLine)
                if eachLineList is not []:
                    wordTagList += eachLineList
            return wordTagList

def processAllFiles(directory):
    finalWordTagList = []
    for eachFile in os.listdir(directory):
        finalWordTagList += processFile(directory+"/"+eachFile)
    return finalWordTagList

def createDictionary(dataList):
    Dictionary = {}
    for data in dataList:
        if data in Dictionary:
            Dictionary[data] += 1
        else:
            Dictionary[data] = 1
    return Dictionary

def createBiGramDictionary(dataList):
    Dictionary = {}
    for i in range (0 ,len(dataList)-1):
        keyData = dataList[i]+'#'+dataList[i+1]
        if keyData in Dictionary:
            Dictionary[keyData] += 1
        else:
            Dictionary[keyData] = 1
    return Dictionary

def clearWords(wordTagList):
    tagList = []
    for wordTag in wordTagList:
        getTag = wordTag.split('/')
        tagList += [getTag[1]]
    return tagList

# gives the transition probability of a given tag t[i-1] and next tag t[i]
def transitionProbability(givenTag, nextTag, tagUniGramDictionary, tagBiGramDictionary):
    biGramKey = givenTag + '#' + nextTag
    probability = float(tagBiGramDictionary[biGramKey])/float(tagUniGramDictionary[givenTag])
    return probability

directory = 'brown copy'
wordTagList = processAllFiles(directory)

#word/tag counts are in this dictionary
WordTagDictionary = createDictionary(wordTagList)

tagList = clearWords(wordTagList)

#tag unigram counts are in this dictionary
tagUniGramDictionary = createDictionary(tagList)
#tag bigram counts are in this dictionary 
tagBiGramDictionary = createBiGramDictionary(tagList)

print(transitionProbability('.', '<EOS>', tagUniGramDictionary, tagBiGramDictionary))