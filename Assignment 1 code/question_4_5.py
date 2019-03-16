import re
import os
from collections import OrderedDict
import numpy as np

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

def clearTags(wordTagList):
    wordList = []
    for wordTag in wordTagList:
        getTag = wordTag.split('/')
        wordList += [getTag[0]]
    return wordList

# gives the transition probability of a given tag t[i-1] and next tag t[i]
def transitionProbability(givenTag, nextTag, tagUniGramDictionary, tagBiGramDictionary):
    biGramKey = str(givenTag) + '#' + str(nextTag)
    probability = 0.0
    vocabulary = len(tagUniGramDictionary)
    if biGramKey in tagBiGramDictionary:
        if givenTag in tagUniGramDictionary:
            probability = float(tagBiGramDictionary[biGramKey] + 0.1)/float(tagUniGramDictionary[givenTag]+ (0.1 * vocabulary))
        else:
            probability = float(tagBiGramDictionary[biGramKey] + 0.1)/float(0.1 * vocabulary)
    else:
        if givenTag in tagUniGramDictionary:
            probability = float(0.1)/float(tagUniGramDictionary[givenTag])
        else:
            probability = float(0.1)/float(0.1 * vocabulary)
    return probability

# gives the emission probability of a given tag t[i-1] and next tag t[i]
def emissionProbability(givenWord, givenTag, WordTagDictionary, tagUniGramDictionary):
    wordTagKey = str(givenWord) + '/' + str(givenTag)
    probability = 0.0
    vocabulary = len(tagUniGramDictionary)
    if wordTagKey in WordTagDictionary:
        if givenTag in tagUniGramDictionary:
            probability = float(WordTagDictionary[wordTagKey] + 0.1)/float(tagUniGramDictionary[givenTag]+ (0.1 * vocabulary))
        else:
            probability = float(WordTagDictionary[wordTagKey])/float(0.1 * vocabulary)
    else:
        if givenTag in tagUniGramDictionary:
            probability = float(0.1)/float(tagUniGramDictionary[givenTag])
        else:
            probability = float(0.1)/float(0.1 * vocabulary)
    return probability

directory = 'brown copy'
wordTagList = processAllFiles(directory)

#word/tag counts are in this dictionary
WordTagDictionary = createDictionary(wordTagList)

gettagList = clearWords(wordTagList)
getwordList = clearTags(wordTagList)

#tag unigram counts are in this dictionary
tagGramDictionary = createDictionary(gettagList)

#word unigram counts are in this dictionary
wordGramDictionary = createDictionary(getwordList)

#tag bigram counts are in this dictionary 
tagBiGramDictionary = createBiGramDictionary(gettagList)


#tag unigram counts are in this dictionary
tagUniGramDictionary = {}
tagList = []

for field, possible_values in tagGramDictionary.items():
    if possible_values > 5:
        tagUniGramDictionary[field] = possible_values
        tagList += [field]
        
tagList = list(OrderedDict.fromkeys(tagList))

#word unigram counts are in this dictionary
wordUniGramDictionary = {}
wordList = []
wordUniGramDictionary['UNK'] = 0

for field, possible_values in wordGramDictionary.items():
    if possible_values > 3:
        wordUniGramDictionary[field] = possible_values
        wordList += [field]
    else:
        wordUniGramDictionary['UNK'] += possible_values
        wordList += ['UNK']

wordList = list(OrderedDict.fromkeys(wordList))

transProbMatrix = {}

for i in range(0, len(tagList)):
    transProbMatrix[tagList[i]] = {}
    for j in range(0, len(tagList)):
        transProbMatrix[tagList[i]][tagList[j]] = 0

for i in range(0, len(tagList)):
    for j in range(0,len(tagList)):
        transProbMatrix[tagList[i]][tagList[j]] = transitionProbability(tagList[i], tagList[j], tagUniGramDictionary, tagBiGramDictionary)

emmiProbMatrix = {}

for i in range(0, len(wordList)):
    emmiProbMatrix[wordList[i]] = {}
    for j in range(0, len(tagList)):
        emmiProbMatrix[wordList[i]][tagList[j]] = 0

for i in range(0, len(wordList)):
    for j in range(0,len(tagList)):
        emmiProbMatrix[wordList[i]][tagList[j]] = emissionProbability(wordList[i], tagList[j], WordTagDictionary, tagUniGramDictionary)

# test file import and cleaning
testFile = 'humor.txt'
sentenceForm = r"[.?!]"

with open(testFile,"r+", encoding=fileEncoding) as testFile:
            storeFileData = testFile.read()
            #storeFileData = re.sub(r"\r! !+", "!", storeFileData)
            SentenceList = re.split(sentenceForm, storeFileData)

def applyViterbi(sentence):
    wordSentence = sentence.split()
    words = []

    for eachWord in wordSentence:
        if eachWord not in wordList:
            words += ['UNK']
        else:
            words += [eachWord]

    startTag = '<sentence>'
    T = len(words)
    N = len(tagList)
    generatedTags = []
    viterbi = np.full((N+2, T), -1)
    backpointer = np.full((N+2, T), -1)

    for s in range(0,N):
        viterbi[s,0] = transProbMatrix[startTag][tagList[s]] + emmiProbMatrix[words[0]][tagList[s]]
        backpointer[s,0] = 0
    
    for t in range(1,T):
        for s in range(1,N):
            for x in range(1,N):
                listVal = []
                listVal += [transProbMatrix[tagList[s]][tagList[x]] * emmiProbMatrix[words[t]][tagList[s]]]
            maxList = max(listVal)
            viterbi[s,t] =viterbi[x,t-1] * maxList
            maxListIndex = listVal.index(maxList)
            backpointer[s,t] = maxListIndex

    indexTag = np.argmax(viterbi[:,-1])
    for y in range(1,T-1):
        intIndexTag = int(indexTag)
        indexTag = backpointer[intIndexTag, y]
        generatedTags += [tagList[intIndexTag]]
    return generatedTags

listOfSentences = []
for eachSentence in SentenceList:
    if eachSentence is not ' ' and eachSentence is not '' and len(eachSentence) > 1 :
        listOfSentences += [eachSentence]

with open('humor_output.txt',"w+", encoding=fileEncoding) as output:
    for index in range(0,len(listOfSentences)-1):
        output.write('<sentence ID = {0}> \n'.format(index+1))
        tags = applyViterbi(listOfSentences[index])
        print(index+1)
        words = listOfSentences[index].split()
        for printIndex in range(0,len(tags)):
            output.write('{0},{1}\n'.format(words[printIndex],tags[printIndex]))
        output.write('<EOS>\n')