import nltk
import sys
import os
import math
from nltk.corpus import stopwords
from collections import Counter

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
    #query = set(tokenize("What are the types of supervised learning?"))
    
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
    material = dict()
    os.chdir(directory)
    pwd = os.getcwd()
    print(f"inside {pwd}")
    for file in os.listdir():
        with open(file, encoding="utf8") as f:
            material[file] = f.read().replace("/n"," ")
            f.close()
    print("Done Loading") 
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
    words = [word.lower() for word in nltk.tokenize.word_tokenize(document) if word.isalpha() or word.isnumeric()]# if word not in nltk.corpus.stopwards.words("english") ]
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
    for sentence in documents:
        contents = documents[sentence]
        for word in contents :
            if word in idfs.keys():
                continue
            else :
                #f = Counter(nltk.ngrams(documents,1))
                #f = sum(word in contents)
                #total = sum
                #f = sum([1 for temp in documents if word in documents[temp]])
                c = 0
                t = 0
                for tmp in documents:
                    if word in documents[tmp]:
                        c += 1
                    t += 1
                idf = math.log(t / c)
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
        for word in query:
            idf = idfs[word]
            s += files[file].count(word)*idf
        tfidfs[file] = s
    return tfidfs

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
        wc = sum( words.count(word) for word in query)
        total = sum( idfs[word] for word in query if word in words)
        ts[sentence] = (total,wc/len(words))
    ts = sorted(ts.keys(),key= lambda x : ts[x] , reverse= True)
    if len(ts) < n:
        return list(ts)
    else :
        ts = list(ts)
        return ts[:n]
        



if __name__ == "__main__":
    main()
