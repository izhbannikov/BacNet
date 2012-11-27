# -*- coding:utf8 -*-
#!/usr/bin/env python

from xml.dom.minidom import parse
import bacteria
import Abstract

__author__="ilya"
__date__ ="$09.11.2012 12:48:51$"

def read_abstracts_from_xml(filename):
    abstracts = []
    dom = parse(filename)
    Year = '1900'
    ArticleTitle = ""
    AbstractText = ""
    AuthorList = ""
    ArticleId = "NA"
    index = 0
    for PubmedArticle in dom.getElementsByTagName('PubmedArticle'):
       AuthorList = ""
       #Publication year
       if len(PubmedArticle.getElementsByTagName('PubDate')[0].getElementsByTagName('Year')) == 0 :
           Year = 1900
       else :
           Year = PubmedArticle.getElementsByTagName('PubDate')[0].getElementsByTagName('Year')[0].firstChild.nodeValue.encode('utf-8')
           #print Year
       #Publication title
       if len(PubmedArticle.getElementsByTagName('ArticleTitle')) == 0 :
           ArticleTitle = "NA"
       else :
           ArticleTitle = PubmedArticle.getElementsByTagName('ArticleTitle')[0].firstChild.nodeValue.encode('utf-8')
           #print ArticleTitle
       #Publication abstract
       if len(PubmedArticle.getElementsByTagName('AbstractText')) == 0 :
           AbstractText = "NA"
       else :
           AbstractText = PubmedArticle.getElementsByTagName('AbstractText')[0].firstChild.nodeValue.encode('utf-8')
           #print AbstractText
       #AuthorList
       for Author in PubmedArticle.getElementsByTagName('Author') :
           AuthorList += Author.getElementsByTagName('LastName')[0].firstChild.nodeValue.encode('utf-8') + ", "

       if len(PubmedArticle.getElementsByTagName('ArticleId')) < 2 :
           ArticleId = "NA"
       else :
           ArticleId = PubmedArticle.getElementsByTagName('ArticleId')[1].firstChild.nodeValue.encode('utf-8')
           #print ArticleId

       abstract = Abstract.Abstract()
       abstract.AuthorList = AuthorList
       abstract.Year = Year
       abstract.ArticleId = ArticleId
       abstract.AbstractText = AbstractText
       abstract.ArticleTitle = ArticleTitle
       abstract.index = index
       abstracts.append(abstract)
       index += 1

    return abstracts

def make_bacteria_dict(filename):    # write Fibonacci series up to n
    bacteria_lst = []
    file = open(filename)
    while 1:
      line = file.readline()
      if not line:
        break
      bnode = BacteriaNode()
      bnode.bac_name = line.strip()
      bacteria_lst.append( bnode )
      global n
      n+=1

    return bacteria_lst