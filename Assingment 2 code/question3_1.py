import os
import re

#3.1 question

def processLine(eachLine):
    wordTagList = []
    if eachLine is not "\n":
        wordTagList = eachLine.split()
    return wordTagList

def processFile(eachFile):
    with open(eachFile,"r+", encoding="latin1") as theFile:
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
        if not eachFile.endswith(".DS_Store"):
            finalWordTagList += processFile(directory+"/"+eachFile)
    return finalWordTagList

def clearTags(wordTagList):
    wordList = []
    for wordTag in wordTagList:
        getTag = wordTag.split('/')
        wordList += [getTag[0].lower()]
    return wordList

directory = "Brown subset"

wordTagList = processAllFiles(directory)

wordList = clearTags(wordTagList)

wordSet = set(wordList)

#print(len(wordList))
#print(len(wordSet))

wordCounts = {}
wordCounts["UNK"] = 0

for each in wordSet:
    count = wordList.count(each)
    if count < 11:
        wordCounts["UNK"] += count
    else:
        wordCounts[each] = count

#for each in wordCounts:
#    print(each+ " ",wordCounts[each])

#print(wordSet)
finalList = [[key,value] for (key, value) in sorted(wordCounts.items(), key=lambda x: (-x[1], x[0]))]

#print(len(wordList))
#print(len(wordSet))
#print(len(wordCounts))

writeFile = "output3_1.txt"

with open(writeFile,"w", encoding="latin1") as theFile:
    for each in finalList:
        theFile.write(each[0] + " "+str(each[1])+"\n")

print("please check output3_1.txt for the output")
