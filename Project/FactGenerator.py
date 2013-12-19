from nltk import word_tokenize
import pickle
import re
from nltk import RegexpParser
from nltk import sent_tokenize

chunks = []
subject = None

#constructs a RegexpParser based on the specified grammar to chunk texts.
def make_chunker():
    grammar = r"""
DATE: {<NNP><CD><NN>}        #Chunk dates of the form Month, Day, Year
NP: {<JJ|NN.*>+<IN><JJ|NN.*>+}# Chunk noun phrases.
      {<JJ|NN.*>+}
      {<NP><CC><NP>}
      {<NNP><IN><NNP>}
      {<NNP><NNP>}
VERB: {<VB.*>}                              # Chunk verb
WH: {<WP>|<WRB>}    #Chunk who, when, and where for questions.
"""
    chunker = RegexpParser(grammar, loop=2)
    return chunker

#constructs a RegexpParser based on specified grammar to chunk questions.
def make_question_chunker():
    grammar = r"""
WHE: {<WRB>}    #Chunk when, and where
WHO: {<WP>}                 #Chunk who
SUBJ: {<NNP><NNP>}  #Chunk subject of question
VERB: {<VB.*>}            #Chunk teh verb of the question
"""
    chunker = RegexpParser(grammar, loop = 2)
    return chunker

#chunks the user input file. 
def chunk_it(sentence):
    tagger = make_tagger()
    tokens = word_tokenize(sentence)
    tags = tagger.tag(tokens)
    chunks = make_chunker().parse(tags)
    return chunks

def make_tagger():
    g = open('tagger.pickle','r')
    tagger = pickle.load(g)
    g.close()
    return tagger

def simplify_sent(sentence):
    sentence = sentence.replace(" a "," ",1)
    sentence = sentence.replace(" an "," ",1)
    sentence = sentence.replace(" the "," ")
    sentence = sentence.replace(", "," ")
    return sentence

def editText(filename):
    global subject
    subject = get_subj(filename)
    f = open(filename, 'r')
    text = f.read()
    f.close()
    new_file_name = subject + 'B.txt'
    g = open(new_file_name, 'w')
    sents = sent_tokenize(text)
    for i in range(len(sents)):
        sents[i] = sents[i].replace(' he ', ' '+subject+' ')
        sents[i] = sents[i].replace(' he.', ' '+subject+'.')
        sents[i] = sents[i].replace(' he,', ' '+subject+',')
        sents[i] = sents[i].replace('He ', subject+' ')
        sents[i] = sents[i].replace(' him ', ' '+subject+' ')
        sents[i] = sents[i].replace(' him.', ' '+subject+'.')
        sents[i] = sents[i].replace(' him,', ' '+subject+',')
        sents[i] = sents[i].replace(' himself ', ' '+subject+' ')
        sents[i] = sents[i].replace(' himself.', ' '+subject+'.')
        sents[i] = sents[i].replace(' himself,', ' '+subject+',')
        sents[i] = sents[i].replace(' his ', ' '+subject+" ")
        sents[i] = sents[i].replace(' his.', ' '+subject+".")
        sents[i] = sents[i].replace(' his,', ' '+subject+",")
        sents[i] = sents[i].replace('His ', subject)
        sents[i] = simplify_sent(sents[i])
        g.write(sents[i] + ' ')
    g.close()
    return new_file_name

def get_subj(filename):
    f = open(filename,'r')
    index = f.name.index('.')
    subject = f.name[:index]
    return subject

def chunkTree_to_list(chunk_tree):
    chunkList = []
    count = 0
    for subtree in chunk_tree.subtrees(filter=lambda t: t.node != 'S'):
            if subtree.height() > 2:
                chunkList.insert(count,subtree.flatten())
            else:
                chunkList.insert(count,subtree)
            count = count + 1
    return chunkList

def generateProlog(chunkList):
    verbIndex = None
    #verbIndex should not remain None as every English sentence contains a verb.
    
    for i in range(len(chunkList)): #get the index of the VERB chunk
        elem = chunkList[i]
        if elem.node == 'VERB':
            verbIndex = i
     #checking for DATE to see if need use dateConstructor       
    for i in range(len(chunkList)): 
        elem = chunkList[i]
        if elem.node == 'DATE' and verbIndex != None:	
            fact = dateConstructor(elem, chunkList, verbIndex) #SUBJ(DATE,VERB,NP+).  
            return fact
            
#constructs facts if no DATE was found.
    if verbIndex != None:
        fact = verbNounConstructor(chunkList, verbIndex) 
        return fact          

def dateConstructor(dateNode, chunkList, index):
    factsubject = subject.replace(" ","_")
    fact = factsubject + "("
    tempsubj = ""
    
    for(word, tag) in dateNode.leaves():
        fact = fact + word + "_"
        
    fact = fact +","
    fact = fact.replace("_,",",")
    newList = chunkList[index:]
    
    for i in range(len(newList)):
        if newList[i].node == 'VERB':
            for (word, tag) in newList[i].leaves():
                fact = fact + word + ","
        elif newList[i].node == 'NP':
            for (word, tag) in newList[i].leaves():
                fact = fact + word + "_"
    fact = fact[:len(fact)-1]               
    fact = fact + ").\n"
    fact = fact.lower()
    return fact
    

def verbNounConstructor(chunkList, index):
    factsubject = subject.replace(" ","_")
    fact1 = factsubject + "("
    fact2 = factsubject + "("
    fact = ""
    tempsubj = ""
    postVerbList = chunkList[index:]
    preVerbList = chunkList[:index]
    
    for i in range(len(postVerbList)):  #SUBJ(VERB,NP+).
        if postVerbList[i].node == 'VERB':  #this should be the first chunk found.
            for (word, tag) in postVerbList[i].leaves():
                fact1 = fact1 + word + ","
        elif postVerbList[i].node == 'NP':
            for (word, tag) in postVerbList[i].leaves():
                fact1 = fact1 + word + "_"
            fact1 = fact1 + ","
            fact1 = fact1.replace("_,",",")
                
    fact1 = fact1 + ")."
    fact1 = fact1.replace(",).",").")
    fact1 = fact1 + "\n"
    fact1 = fact1.lower()

    for i in range(len(preVerbList)):   #SUBJ(NP+).
        if preVerbList[i].node == 'NP':
            for (word, tag) in preVerbList[i].leaves():
                fact2 = fact2 + word + "_"
            fact2 = fact2 + ","
            fact2 = fact2.replace("_,",",")
            
    fact2 = fact2 + ")."
    fact2 = fact2.replace(",).",").")
    fact2 = fact2 + "\n"
    fact2 = fact2.lower()
    fact = fact1 + fact2
    return fact

def generatePrologQueries(question):
    subj = ""
    phrase = ""
    tagger = make_tagger()
    chunker = make_question_chunker()
    words = word_tokenize(question)
    tags = tagger.tag(words)
    chunks = chunker.parse(tags)
    chunkList = chunkTree_to_list(chunks)
    if chunkList[0].node == "WHE":
        chunkList = chunkList[1:]       #skip over 'When __' and 'Where __'
    else:
        pass
    for i in range(len(chunkList)):
        if chunkList[i].node == 'VERB':
            for (word, tag) in chunkList[i].leaves():
                phrase = word
        elif chunkList[i].node == 'SUBJ':
            for (word, tag) in chunkList[i].leaves():
                subj = subj+word+"_"
    subj = subj[:len(subj)-1].lower()
    query1 = subj+"(" + "X,"+phrase+").\n"
    query2 = subj+"(" + phrase +",X).\n"
    query3 = subj+"(" + "X," + phrase + ",Y).\n"
    queries = "\n"+ query1 + query2 + query3
    return queries

def generateAnswer(question, result):
    subj = ""
    phrase = ""
    answer = ""
    tagger = make_tagger()
    chunker = make_question_chunker()
    words = word_tokenize(question)
    tags = tagger.tag(words)
    chunks = chunker.parse(tags)
    chunkList = chunkTree_to_list(chunks)
    if chunkList[0].node == "WHE":
        chunkList = chunkList[1:]       #skip over 'When __' and 'Where __'
    else:
        pass
    for i in range(len(chunkList)):
        if chunkList[i].node == 'VERB':
            for (word, tag) in chunkList[i].leaves():
                phrase = word
        elif chunkList[i].node == 'SUBJ':
            for (word, tag) in chunkList[i].leaves():
                subj = subj+word+"_"
    subj = subj[:len(subj)-1]
    answer = subj + " " + phrase + " " + result + "."
    answer = answer.replace("_"," ")
    return answer

if __name__ == "__main__":  
    import sys                              
    FactGenerator(int(sys.argv[1]))
