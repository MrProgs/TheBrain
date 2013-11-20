#by Sean Daly
# last modified: 11/19/13

import re
#simplifies conjoined sentences.
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

#Domain: Whitehouse.gov presidents biographies.

"""how to get the subject: Get the name of the file. Since my domain is the presidents, I'll have,
as the name of each file, the name of the president. Then I can grab the name of president from
that and use it to replace every instance of he, him, his with name, name, name's."""

def get_subj(filename):
    f = open(filename,'r')
    index = f.name.index('.')
    subject = f.name[:index]
    f.close()
    return subject

def replace_pronouns(filename):
    subj = get_subj(filename)
    f = open(filename, 'r')
    text = f.read()
    f.close()
    new_file_name = subj + 'B.txt'
    g = open(new_file_name, 'w')
    sents = sent_tokenize(text)
    for i in range(len(sents)):
        sents[i] = sents[i].replace(' he ', ' '+subj+' ')
        sents[i] = sents[i].replace(' he.', ' '+subj+'.')
        sents[i] = sents[i].replace(' he,', ' '+subj+',')
        sents[i] = sents[i].replace(' He ', ' '+subj+' ') #why this no work?!
        sents[i] = sents[i].replace(' him ', ' '+subj+' ')
        sents[i] = sents[i].replace(' him.', ' '+subj+'.')
        sents[i] = sents[i].replace(' him,', ' '+subj+',')
        #need to include replacement for himself
        sents[i] = sents[i].replace(' his ', ' '+subj+"'s ")
        sents[i] = sents[i].replace(' his.', ' '+subj+"'s.")
        sents[i] = sents[i].replace(' his,', ' '+subj+"'s,")
        sents[i] = sents[i].replace(' His ', ' '+subj+"'s ")
        g.write(sents[i] + ' ')
    g.close()

if __name__ == "__main__":      # I can't remember what this does. I think
    import sys                              # it has something to do with modules.
    scrapCode(int(sys.argv[1]))


