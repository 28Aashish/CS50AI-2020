import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    
    corpus = crawl(sys.argv[1])
    #corpus=crawl("corpus0")
    
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #raise NotImplementedError
    #Making Model
    model = dict()
    links = len(corpus[page])
    #Checking Links
    if links != 0:
        # Calculaing Constants as per formula
        for link in corpus:
            model[link] = (1-damping_factor)/len(corpus)
        for link in corpus[page]:
        #Calculating recurring Factor as pr formula
            model[link] += damping_factor/links
    else :
        #Equal Probabilty Distribution
        for link in corpus:
            model[link] = 1/len(corpus)
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #raise NotImplementedError
    #Sampling Method
    model = dict()
    for page in corpus:
        model[page]=0
    page =  random.choice(list(corpus.keys()))
    #taking N Samples from From Choices
    for i in range(n):
        oldmodel = transition_model(corpus,page,damping_factor)
        for page in corpus:
            model[page] = (i*model[page]+oldmodel[page])/(i+1)
        page = random.choices(list(model.keys()),list(model.values()),k=1)[0]
    return model


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #raise NotImplementedError
    #From Pagerank Iterative Method
    Rank = dict()
    for page in corpus:
        Rank[page]=1/len(corpus)
    diff = True
    #Loop Till Deviation is less then 0.01%
    #High Accuracy as Probabilty in range 1 to 0 thats Y 0.01% will be accurate enough
    while diff:
        oldRank = Rank.copy()
        diff =False
        for page in corpus:
            #Formula as per Larry Page's Suggested
            Rank[page] = (1-damping_factor)/len(corpus) + damping_factor*adder(corpus,oldRank,page)
            diff = diff or (abs(oldRank[page]-Rank[page]) > 0.0001 ) 

    return Rank

def adder(corpus,oldRank,page):
    total = 0
    for pages in corpus:
        if page in corpus[pages]:
            total += oldRank[pages]/len(corpus[pages])       
    return total

def normalise(Rank):
    total = 0
    for page in Rank:
        total += Rank[page]        
    for page in Rank:
        Rank[page] /= total

    return Rank
if __name__ == "__main__":
    main()
