#!/usr/bin/env python
__author__="ilya"
__date__ ="$01.11.2012 03:08:31$"

import sys
import nltk

keyword_candidates = []
cooccurrence_matrix = []
words = dict()

def make_keyword_candidates(text):
    global keyword_candidates
    global cooccurrence_matrix
    global words
    keyword_candidates = []
    cooccurrence_matrix = []
    words = dict()
    pattern = "NP:{<VB|VBN|JJ|JJR>*<NN|NNS|NNP>*}"
    NPChunker = nltk.RegexpParser(pattern)
    sentences = text.split('. ')
    for sentence in sentences :
        tokens = nltk.word_tokenize(sentence)
        tags = nltk.pos_tag(tokens)
        result = NPChunker. parse(tags)
        #print result
        for n in result:
          if isinstance(n, nltk.tree.Tree):
            if n.node == 'NP':
                kcand = ""
                for item in n.leaves() :
                    kcand+= item[0] + ' ' if len(item[0]) >= 3 else ''
                #print kcand
                if len(kcand) > 3 :
                    keyword_candidates.append(kcand.strip())

    
    

def make_cooccurrence_matrix():
    global cooccurrence_matrix
    global keyword_candidates
    #print keyword_candidates
    global words
    
    for item in keyword_candidates :
        ii = item.split(' ')
        for i in ii :
            words[i] = 1

    for i in xrange(len(words)):
      cooccurrence_matrix.append([])
      for j in xrange(len(words)):
        cooccurrence_matrix[i].append(0)
    wkeys = list(words)
    for i in xrange(len(words)) : #Row
        for z in xrange(len(keyword_candidates)) :
            if wkeys[i] in [kc.strip() for kc in keyword_candidates[z].split(' ') ] :
                for j in xrange(len(words)) : # Column
                    if wkeys[j] in [kc.strip() for kc in keyword_candidates[z].split(' ') ] :
                        cooccurrence_matrix[i][j]+=1
                        

           

    #print_cooccurrence_matrix()

def make_keywords_list():
    global cooccurrence_matrix
    global keyword_candidates
    global words
    word_freqs = dict()
    word_deg = dict()
    score_array = dict()
    keywords = dict()
    
    wkeys = list(words)
    
    for i in xrange(len(cooccurrence_matrix)) :
        deg = 0.0
        for j in xrange(len(cooccurrence_matrix)) :
            deg += cooccurrence_matrix[i][j]
            if i == j :
                word_freqs[wkeys[i]] = cooccurrence_matrix[i][j]
        word_deg[wkeys[i]] = deg

    for i in xrange(len(cooccurrence_matrix)) :
        score_array[wkeys[i]] = word_deg[wkeys[i]]/word_freqs[wkeys[i]]

    #print word_freqs
    #print word_deg
    #print sorted(score_array.items(), key=lambda x: x[1], reverse = True)
    for i in xrange(len(keyword_candidates)) :
        keywords[keyword_candidates[i]] = 0
    
    for i in xrange(len(score_array)) :
        for j in xrange(len(keyword_candidates)) :
            if keyword_candidates[j].rfind(wkeys[i]) != -1 :
                keywords[keyword_candidates[j]] += score_array[wkeys[i]]
                #print score

        

    #print sorted(keywords.items(), key=lambda x: x[1], reverse = True)
    keywords_keys = []
    #print "The list of key words:"
    i = 0
    l = len(keywords)
    for item in list( sorted(keywords.items(), key=lambda x: x[1], reverse = True)) :
        keywords_keys.append(item[0])
        i+=1
        if i > l/3 +1 : break

    return keywords_keys

def print_cooccurrence_matrix() :
   #sss = ""
   #for i in xrange(n) :
   #    sss+= bacteria_lst[i].bac_name.rjust(15)

   #print sss.rjust(70) + "\n"
   global cooccurrence_matrix
   print cooccurrence_matrix
   """global cooccurrence_matrix
   row=0
   col=0
   while row<len(cooccurrence_matrix)-1:
        col=0
        tstr = ""
        while col<len(cooccurrence_matrix)-1:
            tstr+= str(cooccurrence_matrix[row][col]).rjust(15)
            #col=col+1
            #print col
        #print bacteria_lst[row].bac_name.ljust(15-len(bacteria_lst[row].bac_name))+tstr + "\n"
        print tstr
        row=row+1"""