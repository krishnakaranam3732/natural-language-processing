import os
import re


#3.2 question

def clearTags(wordTagList):
    wordList = []
    for wordTag in wordTagList:
        getTag = wordTag.split('/')
        wordList += [getTag[0].lower()]
    return wordList

def processSentences(eachFile):
    with open(eachFile,"r+", encoding="latin1") as theFile:
        storeFileData = theFile.readlines()
        sentenceList = []
        for eachLine in storeFileData:
            eachLine = re.sub(r'\s+', ' ', eachLine)
            if eachLine is not " ":
                listEach = eachLine.split()
                eachLineList = clearTags(listEach)
                if eachLineList is not []:
                    sentence = ''
                    for word in eachLineList:
                        sentence += str(word) + " "
                    sentence = re.sub(r'\.\s', '', sentence)
                    sentenceList += [sentence]
        return sentenceList

def getAllSentences(directory):
    finalsentences =[]
    for eachFile in os.listdir(directory):
        if not eachFile.endswith(".DS_Store"):
            finalsentences += processSentences(directory+"/"+eachFile)
    return finalsentences

def getWordList(allSentences):
    wordList = []
    for sentence in allSentences:
        words = sentence.split()
        for word in words:
            #if word != 'START' and word != 'END':
            wordList += [word]
    return wordList

directory = "Brown subset"
allSentences = getAllSentences(directory)

wordList = getWordList(allSentences)
wordSet = set(wordList)

wordCounts = {}
wordCounts["UNK"] = 0

for each in wordSet:
    count = wordList.count(each)
    if count > 10:
        wordCounts[each] = count
    else:
        wordCounts["UNK"] += count

sentencesFinal = []

for sentence in allSentences:
    wordList = sentence.split()
    include = ''
    for word in wordList:
        if word in wordCounts:
            include += word+" "
        else:
            include += "UNK "
    include = "START "+include+"STOP"
    sentencesFinal += [include]

#print(sentencesFinal)
writeFile = "output3_2_sent.txt"

with open(writeFile,"w", encoding="latin1") as theFile:
    for each in sentencesFinal:
        theFile.write(str(each)+"\n")

print("please check output3_2_sent.txt for the output")

finalList = [[key,value] for (key, value) in sorted(wordCounts.items(), key=lambda x: (-x[1], x[0]))]

writeFile = "output3_2_vocab.txt"

with open(writeFile,"w", encoding="latin1") as theFile:
    for each in finalList:
        theFile.write(str(each[1])+"/"+each[0]+"\n")

print("please check output3_2_vocab.txt for the output")

#finalList = [[key,value] for (key, value) in sorted(wordCounts.items(), key=lambda x: (-x[1], x[0]))]

#print(len(wordList))
#print(len(wordSet))
#print(len(wordCounts))

#for each in finalList:
#    print(each[0] + " ",each[1])