import os
import nltk
import re
import operator
from nltk.parse.stanford import StanfordParser
from nltk.tag.stanford import StanfordPOSTagger,CoreNLPPOSTagger
from nltk import sent_tokenize,word_tokenize
class wordsAndTagsParser(StanfordParser):
    def raw_parse_sents(self, sentences, verbose=False):
        cmd = [
            self._MAIN_CLASS,
            '-model', self.model_path,
            '-sentences', 'newline',
            '-outputFormat', 'wordsAndTags',
            ]
        return self._execute(cmd, '\n'.join(sentences), verbose)

class typedDependenciesParser(StanfordParser):
    def raw_parse_sents(self, sentences, verbose=False):
        cmd = [
            self._MAIN_CLASS,
            '-model', self.model_path,
            '-sentences', 'newline',
            '-outputFormat', 'typedDependencies',
            ]
        return self._execute(cmd, '\n'.join(sentences), verbose)

os.environ['JAVAHOME'] = 'C:/Program Files/Java/jdk-9.0.4/bin/java.exe'
os.environ['STANFORD_PARSER'] = 'C:/stanford/stanford-parser-full-2017-06-09/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = 'C:/stanford/stanford-parser-full-2017-06-09/stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models.jar'

path_model = 'C:/stanford/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'
path_jar = 'C:/stanford/stanford-parser-full-2017-06-09/stanford-parser.jar'
path_models_jar = 'C:/stanford/stanford-parser-full-2017-06-09/stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models.jar'

wordsAndTags = wordsAndTagsParser(model_path=path_model, path_to_jar=path_jar, path_to_models_jar=path_models_jar)
parser = StanfordParser(model_path=path_model, path_to_jar=path_jar, path_to_models_jar=path_models_jar)
typedDependencies = typedDependenciesParser(model_path=path_model, path_to_jar=path_jar, path_to_models_jar=path_models_jar)

#a_sentence = "The strongest rain ever recorded in India shut down the financial hub of Mumbai, snapped communication lines, closed airports and forced thousands of people to sleep in their offices or walk home during the night, officials said today."
#sentence_list = [a_sentence]

# words and tags format for stanford parser
#sentences = wordsAndTags.raw_parse_sents(sentence_list)
#print(sentences)

# penn format for stanford parser
#sentences = parser.raw_parse_sents(sentence_list)
#for each in sentences:
#    for one in each:
#        print(one)
#        print()

# typed dependencies format for stanford parser
#sentences = typedDependencies.raw_parse_sents(sentence_list)
#print(sentences)

#1.1 question

def getFileData(filePath,):
    with open(filePath,"r", encoding="latin1") as theFile:
        result = []
        storeFileData = theFile.readlines()
        for each in storeFileData:
            each = re.sub(r'\? \?', '?', each)
            each = re.sub(r'\! \!', '!', each)
            each = re.sub(r'\. \.', '.', each)
            each = re.sub(r'\; \;', ';', each)
            each = re.sub(r'\`\`', '', each)
            each = re.sub(r'\'\'', '', each)
            each = re.sub(r'\s\s', ' ', each)
            result += [each]
        return result

directory = "Brown_tokenized_text"
prepositions = {}

def getWordsandTags(totalData):
    sentences = sent_tokenize(totalData)
    final_sentences = []
    for each in sentences:
        no_punctuation = re.sub(r'[^\w\s]', '', each)
        words = word_tokenize(no_punctuation)
        if(len(words)<50):
            final_sentences += [each]
    result = []
    for each in final_sentences:
        wordtags = wordsAndTags.raw_parse_sents([each])
        result += [wordtags]
    return result

def countVerbs(each):
    tokens = word_tokenize(each)
    for token in tokens:
        token_array = token.split('/')
        if len(token_array) > 1:
            if len(token_array[1]) > 1:
                if token_array[1] == 'IN' or token_array[1] == 'TO':
                    if token_array[0] in prepositions:
                        prepositions[token_array[0]] += 1
                    else:
                        prepositions[token_array[0]] = 1

Result = ''

for eachFile in os.listdir(directory):
    if eachFile.endswith(".txt"):
        fileData = getFileData(directory+"/"+eachFile)
        toPrint = "for the file "+eachFile+", "
        Result += toPrint+"\n"
        print(toPrint)
        verbcount = 0
        wordandTag = []
        for each in fileData:
            wordandTag += getWordsandTags(each)
        for wordTag in wordandTag:
            countVerbs(wordTag)
        sorted_x = sorted(prepositions.items(), key=operator.itemgetter(1))
        sorted_x.reverse()
        toPrint = "the most common preposition counts are: "
        Result += toPrint+"\n"
        print(toPrint)
        for i in range(0,3):
            print(sorted_x[i])
            Result += str(sorted_x[i])+"\n"
        for each in sorted_x:
            verbcount += each[1]
        toPrint = "the total preposition counts are: "+str(verbcount)
        Result += toPrint+"\n\n"
        print(toPrint)

writeFile = "output1_3.txt"

with open(writeFile,"w", encoding="latin1") as theFile:
    theFile.write(Result)

print("please check output1_3.txt for the output")