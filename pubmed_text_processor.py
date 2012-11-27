import nltk.tokenize
#!/usr/bin/env python

import nltk
##from nltk.corpus import brown
import fileinput
import keywords_extractor as kwe

__author__="ilya"
__date__ ="$23.10.2012 15:53:48$"

assepted_tags = ['NN', 'N', 'NNS', 'NNP']#['NN', 'NNP', 'N', 'NNS']
blacklisted_words = []
accepted_words = []
bacteria_words = dict()

def calculate_frequences(text):
    tokens = nltk.word_tokenize(text)
    tags = nltk.pos_tag(tokens)
    tmp_dict = dict()
    for tag in tags :
        if tag[1] in assepted_tags :
            tmp_dict[tag[0]] = 1

    for entity in tmp_dict :
        try:
            bacteria_words[ entity ] += 1
        except :
            bacteria_words[ entity ] = 1

    remove_notneeded_words(0)
    

#Removes unneeded words from bacteria_words dictionary
def remove_notneeded_words(ask_for_assistamce_flag):
    global bacteria_words
    read_accepted_words('accepted_words.txt')
    for entity in bacteria_words :
        if entity in blacklisted_words :
            bacteria_words = removekey(bacteria_words, entity)
            #if len(entity) < 4 :
            #    bacteria_words = removekey(bacteria_words, str(entity) )
        else :
            if len(entity) < 4 :
                bacteria_words = removekey(bacteria_words, str(entity) )
                continue
            if ask_for_assistamce_flag == 1 :
                if entity not in accepted_words :
                    #Ask user if he wants to add a word into blacklisted_words dictionary
                    print "A term '" + str(entity) +"' is not in blacklisted words. Should I put it to them (y/n)?"
                    s = raw_input('--> ')
                    if s == 'y' :
                        bacteria_words = removekey(bacteria_words, str(entity) )
                        blacklisted_words.append(str(entity).lower())
                        continue

                    accepted_words.append(str(entity).lower())
            
   


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def read_blacklisted_words(filename):
    global blacklisted_words
    for line in fileinput.input([filename]):
        blacklisted_words.append(line.lower()[:len(line)-1])

def read_accepted_words(filename):
    global accepted_words
    for line in fileinput.input([filename]):
        accepted_words.append(line.lower()[:len(line)-1])

def write_blacklisted_words(filename):
    global blacklisted_words
    f = open(filename, 'w')
    for item in blacklisted_words:
        f.write(item + '\n')

def write_accepted_words(filename):
    global accepted_words
    f = open(filename, 'w')
    for item in accepted_words:
        f.write(item + '\n')

def calculate_index_words(text):
    #print text
    kwe.make_keyword_candidates(text)
    kwe.make_cooccurrence_matrix()
    return kwe.make_keywords_list()
        