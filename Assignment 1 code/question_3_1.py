import re
import os

directory = "gutenberg"

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

def countNgrams(saveFileName,data,ngram):
    nGramDictionary = {}
    
    for i in range (0 ,len(data)-ngram):
        if data[i:i+ngram] in nGramDictionary:
            nGramDictionary[data[i:i+ngram]] += 1
        else:
            nGramDictionary[data[i:i+ngram]] = 1
    
    with open(saveFileName ,"w+", encoding="latin1") as ngramfile:
        for key in nGramDictionary:
            linewrite = '{0} {1}\n'.format(key,nGramDictionary[key])
            ngramfile.write(linewrite)

data = getAllFilesData(directory)

fourgramfile = "fourgramcount.txt"
fivegramfile = "fivegramcount.txt"

countNgrams(fourgramfile,data,4)
countNgrams(fivegramfile,data,5)