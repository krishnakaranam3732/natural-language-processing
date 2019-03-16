#Brown clustering

import os
import re
import math

sentencesFile = 'output3_2_sent.txt'
vocabFile = 'output3_2_vocab.txt'

stringOutput = 'strings.txt'
clusterOutput = 'clusters.txt'

sentences = []
vocabulary = {}
clusters = {}
clusterString = {}

k = 100

# remove from here 

def getVocabFromSent(sentences):
    vocab = []
    for each in sentences:
        words = each.split()
        words.remove('START')
        words.remove('STOP')
        vocab += words
    return vocab

def getVocabFromS(vocabFile, vocabList):
    vocab = {}
    with open(vocabFile,"r+", encoding="latin1") as theFile:
        storeFileData = theFile.readlines()
        for eachLine in storeFileData:
            eachLine = re.sub(r'\n', '', eachLine)
            tokens = eachLine.split('/')
            if tokens[1] in vocabList:
                vocab[tokens[1]] = tokens[0]
    return vocab

# remove till here

def getSentences(sentencesFile):
    sentenceList = []
    with open(sentencesFile,"r+", encoding="latin1") as theFile:
        storeFileData = theFile.readlines()
        for eachLine in storeFileData:
            eachLine = re.sub(r'\n', '', eachLine)
            sentenceList += [eachLine]
    return sentenceList

def getVocab(vocabFile):
    vocab = {}
    with open(vocabFile,"r+", encoding="latin1") as theFile:
        storeFileData = theFile.readlines()
        for eachLine in storeFileData:
            eachLine = re.sub(r'\n', '', eachLine)
            tokens = eachLine.split('/')
            vocab[tokens[1]] = tokens[0]
    return vocab

def getVocabAsList(vocabFile):
    vocab = []
    with open(vocabFile,"r+", encoding="latin1") as theFile:
        storeFileData = theFile.readlines()
        for eachLine in storeFileData:
            eachLine = re.sub(r'\n', '', eachLine)
            tokens = eachLine.split('/')
            vocab += [tokens[1]]
    return vocab

def calcBigramCounts(sentences):
    bigrams = {}
    for each in sentences:
        wordList = each.split()
        for i in range(0,len(wordList)-2):
            bigram_key = wordList[i]+"#"+wordList[i+1]
            if bigram_key in bigrams:
                bigrams[bigram_key] += 1
            else:
                bigrams[bigram_key] = 1
    return bigrams

def getNumberOfWords(sentences):
    count = 0
    for each in sentences:
        wordList = each.split()
        wordList.remove('START')
        wordList.remove('STOP')
        count += len(wordList)
    return count

# P(cluster1,cluster2)
def getValuePCC(wordCount, cluster1List, cluster2List, biGramCounts):
    NCC = 1
    for c1 in cluster1List:
        for c2 in cluster2List:
            bigram_key = c1+"#"+c2
            if bigram_key in biGramCounts:
                NCC += int(biGramCounts[bigram_key])
    return float(NCC/wordCount)

# q(clusterFollowing/clusterGiven)
def getValuepc(wordCount, clusterList, vocabulary):
    NC = 1
    for each in clusterList:
        if each in vocabulary:
                NC += int(vocabulary[each])
    return float(NC/wordCount)

# calculate quality value of C for the corpus , cluster1 and cluster2
def calcQualityC(wordCount, cluster1List, cluster2List, biGramCounts, vocabulary):
    PCC = getValuePCC(wordCount, cluster1List, cluster2List, biGramCounts)
    PC1 = getValuepc(wordCount, cluster1List, vocabulary)
    PC2 = getValuepc(wordCount, cluster2List, vocabulary)
    result = PCC * math.log(float(PCC/(PC1 * PC2)))
    return result

# Maximize the quality value of C for the corpus and a cluster
def MaximizeQualityC(wordCount, cluster, biGramCounts, vocabulary):
    clusterList = clusters.keys()
    maxQuality = 0
    firstCluster = 0
    secondCluster = 0
    for first in clusterList:
        for second in clusterList:
            if first != second:
                calQual = calcQualityC(wordCount, cluster[first], cluster[second], biGramCounts, vocabulary)
                if(calQual > maxQuality):
                    #print("calQual is: ",calQual)
                    #print("maxQuality is: ",maxQuality)
                    #print("first is:"+str(first)+" second is:"+str(second))
                    maxQuality = calQual
                    firstCluster = first
                    secondCluster = second
    # for every pair of clusters possible, get the C value and store it with clusters
    return [firstCluster,secondCluster]

# list of all sentences
sentences = getSentences(sentencesFile)

# remove this
#sentences = sentences[0:600]

# total number of words
wordCount = getNumberOfWords(sentences)

# BiGram counts for all the words in the sentences
biGramCounts = calcBigramCounts(sentences)

#with open("3_3_bigrams.txt","w", encoding="latin1") as theFile:
#    theFile.write(str(biGramCounts))

#print("check Bigram File")

# dictionary of words and their counts  - remove commenting
vocabulary = getVocab(vocabFile)

# list of the vocabulary set - remove commenting
vocabList = getVocabAsList(vocabFile)

# remove from here

#vocabListFromSent = getVocabFromSent(sentences)
#vocabList = set(vocabListFromSent)
#vocabList = list(vocabList)
#print(vocabList)
#vocabulary = getVocabFromS(vocabFile, vocabList)

# remove till here


# length of the vocabulary set
vocabSetLength = len(vocabList)

# list of top k most common occuring words
vocabListK = vocabList[0:k]

for each in vocabListK:
    clusters[vocabListK.index(each) + 1] = [each]
    
#for i in range(1,vocabSetLength):
#    clusterString[i] = ''

for each in vocabList:
    clusterString[each] = ''

# clusters : { 1 : [word1,word2] }
# clusterString : { 1 : '0100100'}


# Brown Algorithm
for i in range(k+1,vocabSetLength):

    # created new cluster for ith word
    clusters[i] = [vocabList[i-1]]
    # merge two clusters by maximizing the quality of C in clusters
    clusterPair = MaximizeQualityC(wordCount, clusters, biGramCounts, vocabulary)
    #print("***********************************************************************************************")
    print("cluster pair is:"+str(clusterPair)+"vocabSetLength is :"+str(vocabSetLength)+" index is "+str(i))
    #print("***********************************************************************************************")
    #if i == 1000:
    #    print("break done")
    #    break

    first = clusterPair[0]
    second = clusterPair[1]

    # delete the 2nd cluster
    if first != second:
        #update the clusterString values
        for one in clusters[first]:
            clusterString[one] = "0" + clusterString[one]
        for one in clusters[second]:
            clusterString[one] = "1" + clusterString[one]

        clusters[first] += clusters[second]
        del clusters[second]
    else:
        i -=1
        
with open("cluster3_4.txt","w", encoding="latin1") as theFile:
    for key in clusters:
        theFile.write(str(key)+" "+str(clusters[key])+"\n")

print("please check cluster3_4.txt for the output")

with open("string3_4.txt","w", encoding="latin1") as theFile:
    for key in clusterString:
        theFile.write(str(key)+" "+clusterString[key]+"\n")

print("please check string3_4.txt for the output")


for i in range(0,k-1):
    keyList = []
    for key in clusters:
        keyList += [key]

    # merge two clusters by maximizing the quality of C in clusters
    clusterPair = MaximizeQualityC(wordCount, clusters, biGramCounts, vocabulary)
    #print("***********************************************************************************************")
    print("final merge cluster pair is:"+str(clusterPair))
    #print("***********************************************************************************************")
    #if i == 80:
    #    print("break done")
    #    break

    first = clusterPair[0]
    second = clusterPair[1]

    # delete the 2nd cluster
    if first != second:
        #update the clusterString values
        for one in clusters[first]:
            clusterString[one] = "0" + clusterString[one]

        for one in clusters[second]:
            clusterString[one] = "1" + clusterString[one]

        clusters[first] += clusters[second]
        del clusters[second]
    else:
        i -=1


with open(clusterOutput,"w", encoding="latin1") as theFile:
    for key in clusters:
        theFile.write(str(key)+" "+str(clusters[key])+"\n")

print("please check "+clusterOutput+" for the output")


with open(stringOutput,"w", encoding="latin1") as theFile:
    for key in clusterString:
        theFile.write(str(key)+" "+clusterString[key]+"\n")

print("please check "+stringOutput+" for the output")
