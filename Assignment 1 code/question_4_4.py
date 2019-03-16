import re
import os
import random
from collections import OrderedDict

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

tagGramDictionary = createDictionary(gettagList)

#tag bigram counts are in this dictionary
tagBiGramDictionary = createBiGramDictionary(gettagList)

#tag unigram counts are in this dictionary
tagUniGramDictionary = {}
tagList = []

for field, possible_values in tagGramDictionary.items():
    if possible_values > 5:
        tagUniGramDictionary[field] = possible_values
        tagList += [field]

#print(len(tagList))
tagList = list(OrderedDict.fromkeys(tagList))

def createTagToWord(wordTagList):
    tagToWord = {}
    for wordTag in wordTagList:
        getTag = wordTag.split('/')
        if getTag[1] in tagToWord:
            if getTag[0] not in tagToWord[getTag[1]]:
                tagToWord[getTag[1]] += [getTag[0]]
        else:
            tagToWord[getTag[1]] = [getTag[0]]
    return tagToWord

def createWordToTag(wordTagList):
    wordToTag = {}
    for wordTag in wordTagList:
        getTag = wordTag.split('/')
        if getTag[0] in wordToTag:
            if getTag[1] not in wordToTag[getTag[0]]:
                wordToTag[getTag[0]] += [getTag[1]]
        else:
            wordToTag[getTag[0]] = [getTag[1]]
    return wordToTag

tagToWordDictionary = createTagToWord(wordTagList)

wordToTagDictionary = createWordToTag(wordTagList)

def getRandomTag(existingTag, tagList, tagUniGramDictionary, tagBiGramDictionary):
    dupList = tagList
    randomNumber = random.randint(0,len(dupList)-1)
    transProb = transitionProbability(existingTag, dupList[randomNumber], tagUniGramDictionary, tagBiGramDictionary)
    limit = 0.1
    if transProb > limit:
        return [dupList[randomNumber],transProb]
    else:
        return None


def getRandomWord(existingTag, tagToWordDictionary, WordTagDictionary, tagUniGramDictionary):
    tagToWordLen = len(tagToWordDictionary[existingTag])-1
    randomNumber = random.randint(0,tagToWordLen)
    wordList = tagToWordDictionary[existingTag]
    emmiProb = emissionProbability(wordList[randomNumber], existingTag, WordTagDictionary, tagUniGramDictionary)
    limit = 0.001
    if emmiProb > limit:
        return [wordList[randomNumber],emmiProb]
    else:
        return None

#Generate a word given the last word in the sentence generated
def generateNextWord(startTag, tagList):
    tagRandom = None
    while tagRandom is None:
        tagRandom = getRandomTag(startTag, tagList, tagUniGramDictionary, tagBiGramDictionary)
    wordRandom = None
    while wordRandom is None:
        wordRandom = getRandomWord(tagRandom[0], tagToWordDictionary, WordTagDictionary, tagUniGramDictionary)
    return [wordRandom, tagRandom]

def generateSentence():
    startTag = '<sentence>'
    startWord = '<sentence>'
    endTag = '<EOS>'
    endWord = '<EOS>'

    tagGenerated = ''
    wordGenerated = ''
    sentenceGenerated = '<sentence>/<sentence>'

    totalProbability = 0.0 
    while wordGenerated != endWord:
        wordTagGenerated = generateNextWord(startTag, tagList)
        wordGenerated = wordTagGenerated[0][0]
        tagGenerated = wordTagGenerated[1][0]
        emmiProbability = wordTagGenerated[0][1]
        transProbability = wordTagGenerated[1][1]
        startTag = tagGenerated
        sentenceGenerated +=' ' + wordGenerated+'/'+tagGenerated
        if totalProbability < emmiProbability * transProbability:
            totalProbability = emmiProbability * transProbability

    sentenceGenerated = sentenceGenerated + ' Probability: {0}'.format(totalProbability)
    return sentenceGenerated

count = 5
while count > 0:
    print(generateSentence())
    count -= 1