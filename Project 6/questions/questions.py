import nltk
import sys
import os
import math
from nltk.corpus import stopwords
import string

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    #files = load_files("corpus")
    
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    
    query = set(tokenize(input("Query: ")))
    #query = set(tokenize("How do neurons connect in a neural network?"))
    
    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    #raise NotImplementedError
    
    #initialising dictionary
    material = dict()
    #Changing Working directory
    os.chdir(directory)
    pwd = os.getcwd()
    print(f"inside {pwd}")
    #Checking Files in The directorys
    for file in os.listdir():
        with open(file, encoding="utf8") as f:
            material[file] = f.read().replace("/n"," ")
            f.close()
    print("Done Loading") 
    #Back to Old directory
    os.chdir('..')
    
    return material

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    #raise NotImplementedError

    #Words which are alphanumeric only are Considered
    pl = list(nltk.corpus.stopwords.words("English")) + list(string.punctuation)
    words = [word.lower() for word in nltk.tokenize.word_tokenize(document) if word.lower() not in pl ]
    
    return words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    #raise NotImplementedError
    idfs = dict()
    totalDocuments = len(documents)    
    for Doc in documents:
        contents = documents[Doc]
        for word in contents :
            if word in idfs.keys():
                continue
            else :
                count = 0
                for tmp in documents:
                    if word in documents[tmp]:
                        count += 1
                        continue
                idf = math.log(totalDocuments / count)
                idfs[word] = idf   
    return idfs   

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    #raise NotImplementedError

    tfidfs = dict()
    for file in files:
        s = 0
        for word in set(query):
            if word in idfs.keys():
                idf = idfs[word]
                fr = files[file].count(word) 
                s += fr * idf
        tfidfs[file] = s
    tfidf =sorted(tfidfs ,key= lambda x : tfidfs[x] , reverse= True)
    if len(tfidf) < n:
        return tfidf
    else :
        return tfidf[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    #raise NotImplementedError
    ts = dict()
    for sentence in sentences:
        words = sentences[sentence]
        lwords = len(words)

        term =   sum( words.count(word)  for word in set(query))
        idf  =   sum( idfs[word]         for word in set(query) if word in words)

        ts[sentence] = (idf , term/lwords)
    ts =sorted(ts ,key= lambda x : ts[x] , reverse= True)
    if len(ts) < n:
        return list(ts)
    else :
        ts = list(ts)
        return ts[:n]

if __name__ == "__main__":
    main()
