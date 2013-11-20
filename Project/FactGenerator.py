#by Sean Daly
#last modified: 11/19/13
from nltk import word_tokenize
import pickle
import re
from nltk import RegexpParser
from nltk import sent_tokenize
from transforms import filter_insignificant

#constructs a RegexpParser based on the specified grammar
def make_chunker():
    grammar = r"""
NP: {<JJ|NN.*>+}          # Chunk sequences of JJ, NN
PP: {<IN><NP>}               # Chunk prepositions followed by NP
VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
CLAUSE: {<NP><VP>}           # Chunk NP, VP
"""
    #VERB: {<VB.*>}                      # Chunk verbs
    chunker = RegexpParser(grammar, loop=2)
    return chunker

#chunks the user input file. 
def chunk_it(sentence):
    g =open('tagger.pickle', 'r')
    tagger = pickle.load(g)         #loads a pre-trained tagger.
    g.close()
    tokens = word_tokenize(sentence)
    tags = tagger.tag(tokens)
    chunks = make_chunker().parse(tags)
    return chunks

#extracts the first NP from the tree resulting from RegexpParser.
#This works for the sentence formatted as follows: NP VERB NP PP
def np_extract(chunk_tree):
    count = 0
    noun_phrase = ''
    for subtree in chunk_tree.subtrees(filter=lambda t: t.node == 'NP'):
        if count > 1:
            break
        np = subtree
        count = count + 1
        for (word, tag) in np.leaves():
            noun_phrase = noun_phrase+ ' ' + word
        return noun_phrase

#extracts the stand alone verbs from the chunk tree. Stand alone here
#means not part of a VP subtree
def vp_extract(chunk_tree):
    vp = ''
    for subtree in chunk_tree.subtrees(filter=lambda t: t.node == 'VP'):
        verb_phrase = subtree
        for (word, tag) in verb_phrase.leaves():
            vp = word
        return vp

#extracts the prepositional phrase from the chunk tree.
def pp_extract(chunk_tree):
    count = 0
    prep_phrase = ''
    for subtree in chunk_tree.subtrees(filter=lambda t: t.node == 'PP'):
        if count > 1:
            break
        pp = subtree
        count = count + 1
        for (word, tag) in pp.leaves():
            prep_phrase = prep_phrase+ ' '+ word
        print prep_phrase
        return prep_phrase

#returns a Prolog fact based on the provided chunk_tree
def make_Prolog(text_file):
    count = 0
   # facts = ''
    f = open(text_file, 'r')
    text = f.read()
    f.close()
    g = open('facts.pl', 'w')
    sents = sent_tokenize(text)
    for i in range(len(sents)):
        chunk_tree = chunk_it(sents[i])
        p1 = np_extract(chunk_tree)
        print p1
        p1 = p1.replace(' ', '_')
        p2 = verb_extract(chunk_tree)
        print p2
        p2 = p2.replace(' ', '_')
        p3 = pp_extract(chunk_tree)
        print p3
        #p3 = p3.replace(' ', '_')
        fact = '%s(%s,%s).' % (p2, p1, p3)
        g.write(fact)
    return fact

def simplify_sent(sentence):
    sentence = re.sub(r',.*,',"",sentence) #removes non-restrictive appositives, non-restrictive
    print sentence                                  #relative clauses, and participal modifiers of NP's.
    sentence = sentence.replace(" and",".",1)
    sentence = sentence.replace(" but",".",1)
    print sentence.index('.')
    print len(sentence)
    if sentence.index('.') == len(sentence)-1:
        return sentence
    else:
        s = list(sentence)
        index = s.index('.')+2
        s[index] = s[index].upper()
        sentence = "".join(s)
    return sentence

def get_subj(filename):
    f = open(filename,'r')
    index = f.name.index('.')
    subject = f.name[:index]
    return subject


if __name__ == "__main__":      # I can't remember what this does. I think
    import sys                              # it has something to do with modules.
    FactGenerator(int(sys.argv[1]))
