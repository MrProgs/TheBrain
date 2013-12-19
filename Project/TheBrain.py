from FactGenerator import *
from nltk import sent_tokenize, word_tokenize

question = ""
name = ""

def feedTheBrain():
    textfile = ""
    go = True
    while go == True:
        textfile = raw_input("Please enter a file you'd like me to read: (type 'no' to exit) ")
        if textfile != "no":
            consume(textfile)
        else:
            go = False

def askTheBrain():
    global question
    global name
    go = True
    while go == True:
        name = raw_input("Hello. I am The Brain. What is your name?")
        question= raw_input("What would you like to know, "+name+"? (type 'nothing' to quit') ")
        if question != 'nothing':
            query = generatePrologQueries(question)
            print query
        else:
            go = False

def Answer(question, result):
    answer = generateAnswer(question, result)
    print name+", "+answer

def consume(textfile):
    facts = open('presidentFacts.pl','a')
    text = editText(textfile)
    f = open(text, 'r')
    cleanText = f.read()
    f.close()
    sents = sent_tokenize(cleanText)
    tagger = make_tagger()
    chunker = make_chunker()
    for i in range(len(sents)):
        words = word_tokenize(sents[i])
        tags = tagger.tag(words)
        chunk_tree = chunker.parse(tags)
        chunkList = chunkTree_to_list(chunk_tree)
        prologFact = generateProlog(chunkList)
        if prologFact != None:
            facts.write(prologFact)
        else:
            pass

    facts.close()
    

    
