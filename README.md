# natural-language-processing

# Assignment 1 questions:

Question 3. Language Modeling:

3.1 Implement a 5-gram character language model from the following English
training data: http://www.nltk.org/nltk_data/packages/corpora/gutenberg.zip

Remove blank lines from each file. Replace newline characters with spaces, and remove duplicate
spaces. Across all files in the directory (counted together), report the 4-gram and 5-gram
character counts.

3.2 The test dataset is given here: https://www.dropbox.com/s/hpcsp1ifwiwaixg/SOC_new.zip?dl=0
Remove blank lines from the test data, replace newline characters with spaces, and remove
duplicate spaces.
Take the file that is named ”03302 02.txt”. This is an English file. Report the average perplexity
(per character) for this file. Use add-lambda smoothing (with lambda = 0.1).

3.3 Some of the files in the test dataset are not English files. Identify them as follows:
For each file in the directory of test data, calculate the perplexity. Using these scores, report the
names and scores of the three files with the highest perplexity.

Question 4. POS Tagging - HMM - Hidden Markov Models:

The training dataset is a subset of the Brown corpus, where each file contains sentences of
tokenized words followed by POS tags, and where each line contains one sentence: https://www.dropbox.com/s/6y365hoxd7huzbm/browncopy.zip?dl=0

The test dataset (which is another subset of the Brown corpus, containing tokenized words but no
tags) is the following: https://www.dropbox.com/s/hk6uk5amkf6ubww/humor.txt?dl=0
Implement a part-of-speech tagger using a bigram HMM. 
Use Viterbi algorithm for decoding (eq. 10.9 in book - http://web.stanford.edu/˜jurafsky/slp3/10.pdf).

4.1 Obtain frequency counts from the collection of all the training files (counted
together). You will need the following types of frequency counts: word/tag counts, tag unigram
counts, and tag bigram counts. Let’s denote these by C(wi, ti), C(ti), and C(ti−1, ti),
respectively. Report these quantities.
To obtain the tag unigram counts and the tag bigram counts, you will need to separate out each
tag from its word. For each sentence found in the training data, add a start token and an end token
to the beginning and the end of the sentence.

4.2 A transition probability is the probability of a tag given its previous tag. Calculate
transition probabilities of the training set.

4.3 An emission probability is the probability of a given word being associated with a
given tag. Calculate emission probabilities of the training set.

4.4 Generate 5 random sentences using HMM. Output each sentence (with the POS
tags) and its probability of being generated.

4.5 Split the test data into sentences. For each word in the test dataset, derive the most
probable tag sequence using the Viterbi algorithm; pseudocode can be found in the textbook
(http://web.stanford.edu/˜jurafsky/slp3/10.pdf) under Figure 10.8.
For each word, output the tag derived using the Viterbi algorithm in the following format
(where each line contains no more than one pair):
<sentence ID=1> word, tag word, tag ... word, tag <EOS>
<sentence ID=2> word, tag word, tag ... word, tag <EOS>


# Assignment 2 questions:

Question 1. Parsing:

Using Version 3.8.0 of the Stanford parser (https://nlp.stanford.edu/software/lex-parser.shtml#History), parse the following corpus, where each file represents one genre of text:
www.dropbox.com/s/9t5xifk5erssdn0/Brown_tokenized_text.zip?dl=0
For sentences containing 50 words or less (punctuation does not count), obtain the part-of-speech
tags, the context-free phrase structure grammar representation, and the typed dependency
representation as shown in the following sample output:
https://nlp.stanford.edu/software/lex-parser.shtml#Sample

1.1 Using the part-of-speech tags that the parser has given you, report the number of
verbs in each file. Also report the part-of-speech tags that you are using to identify the verbs.

1.2 Report the number of sentences parsed; do so by searching for “ROOT” in either the dependency representation or in the context-free phrase structure grammar representation.

1.3 Using the dependency representation (or the context-free phrase structure grammar
representation) that the parser has given you, report the total number of prepositions found in each
file. In addition, report the most common three preposition overall.

1.4 Take a look at the constituent parsing and dependency parsing results. List out two
common errors made in each type of parsing results, and briefly discuss potential methods to
reduce each type of error.

Question 3. Brown Clustering:

A subset of the Brown corpus (already tokenized) is given here:
www.dropbox.com/s/0k3dn901ergqge0/Brown%20subset.zip?dl=0

3.1 Remove the part-of-speech tags appended to each token. Lowercase all words.
Replace all tokens with a count of 10 or less with the out-of-vocabulary symbol UNK. Sort the
vocabulary by decreasing frequency and then alphabetically (to break ties). Submit this ranked
vocabulary list; include the counts for all words in your submission.

3.2 For purposes of the bigram model, treat each sentence on its own line as
independent of the others, and assume that each sentence begins and ends with invisible START
and END symbols. (However, these symbols should not be included in the clustering.) Turn in
your code that takes your vocabulary and the corpus as input.

3.3 Implement Brown clustering on the given dataset. Let K = 100 be the initial
number of clusters. You should therefore give each of the 100 most frequent tokens its own
cluster and proceed as described above. The output will consist of the same vocabulary with a
string of 0’s and 1’s corresponding to each vocabulary item, indicating its path from the root of
the cluster merge tree to the leaves. Since the clusters start out sorted by decreasing frequency, we
stipulate that when merging two clusters, the earlier cluster on the list gets the code 0 and the later
cluster gets the code 1.
For a tutorial on Brown clustering, refer to the recordings in this playlist:
https://www.youtube.com/watch?v=xGfQMrYoIx4&list=PLO9y7hOkmmSEAqCc0wrNBrsoJMTmIN98M
Along with your code, submit a file named strings.txt that contains the binary strings
corresponding to all the vocabulary items, and report all the clusters with their respective words in
a file named clusters.txt.

3.4 Convert each vocabulary item into a vector using tools of your choice. Next,
compute the cosine distance between every pair of words in each cluster. Report the average
cosine distance for each of your clusters.

CLEANING EXAMPLE:
“The/at Fulton/np-tl County/nn-tl Grand/jj-tl Jury/nn-tl said/vbd Friday/nr an/at investigation/nn
of/in Atlanta’s/np recent/jj primary/nn election/nn produced/vbd “/“ no/at evidence/nn ”/” that/cs
any/dti irregularities/nns took/vbd place/nn ./.”
should become
“START the fulton county grand jury said friday an UNK of UNK UNK primary election UNK
no evidence that any UNK took place STOP”

Question 5. Multilayer Perceptron:

The following training dataset contains SMS messages, where each message is followed by a
label (which is preceded by a comma) for whether the message is considered spam (or “ham”, the
opposite of “spam”): www.dropbox.com/s/edtb5mqnbw7dd1u/train_english_spam.txt?dl=0

Using the tool of your choice (suggestions are listed below), train a Multilayer Perceptron to
detect spam messages. 
Call the training and testing functions for the Multilayer Perceptron fromthe tool. You do not need to implement the learning (i.e., backpropagation) algorithm. 
You should have an input layer, two hidden layers, and an output layer; the second hidden layer should have 10 nodes. Use 10-fold cross-validation to optimize any parameters (e.g. activation function or
number of nodes in the first hidden layer). 
Explain what parameters you have tried and report the precision and recall from cross-validation for the design yielding the best performance.

The following test set contains 300 messages only (without labels), one message per line:
www.dropbox.com/s/s2ui8muihqcgsmz/test_data_english_spam.txt?dl=0

Predict the labels for all the messages in the test set using your best classifer built above. Submit
these 300 predictions in a file named labels.txt. Each line should contain the prediction (which is
either spam or ham) for the corresponding line of the test dataset.
Tool suggestions:
• TensorFlow https://www.tensorflow.org/
• theano http://deeplearning.net/software/theano/
• Weka https://www.cs.waikato.ac.nz/˜ml/weka/
• scikit-learn http://scikit-learn.org/stable/index.html
• PyTorch http://pytorch.org/

