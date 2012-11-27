# -*- coding:utf8 -*-
#!/usr/bin/env python

import sys
import csv
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import getopt
from xml.dom.minidom import parse
import time_layer as tl
import bacteria
import Abstract
import keywords_extractor as kwe
import QueryItem

bacteria_lst = []
abstracts = []
n = 0
a_matrix = []
a_matrix_words = []
pos = []

def read_txt_file(filename):    # write Fibonacci series up to n
    array = []
    file = open(filename)
    while 1:
      line = file.readline()
      if not line:
        break
      query_item = QueryItem.QueryItem()
      query_item.name = line.strip()
      query_item.key_words = dict()
      array.append(query_item)
    return array
    
def make_bacteria_dict(filename):    # write Fibonacci series up to n
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
      #print line
    #print n	
    
def read_csv(filename) :   
  with open(filename, 'rb') as csvfile:
    abstract_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for abstract in abstract_reader:
      abstracts.append(abstract[1])
      #print row[1]


def make_adj_matrix() :
  for i in xrange(n):
    a_matrix.append([])
    for j in xrange(n):
      a_matrix[i].append(0)
  #print n
  for i in xrange(n) :
    for z in xrange(len(abstracts)) :
      if ( (abstracts[z].AbstractText.rfind( bacteria_lst[i].bac_name )) != -1 )  :
        bacteria_lst[i].Freq += 1
        #print bacteria_lst[i].Freq
	for j in xrange(n) :
            if ((abstracts[z].AbstractText.rfind( bacteria_lst[j].bac_name) != -1)  and (i != j) )  :
                a_matrix[i][j]+=1
                continue
        
     #continue
    if (bacteria_lst[i].Freq == 0) :
       bacteria_lst[i].Freq = 1
    
    
  #print a_matrix 
  
  

def print_adj_matrix() :
   sss = ""
   for i in xrange(n) :
       sss+= bacteria_lst[i].bac_name.rjust(15)

   print sss.rjust(70) + "\n"
       
   row=0
   col=0
   while row<n:
    col=0
    tstr = ""
    while col<n:
     tstr+= str(a_matrix[row][col]).rjust(15)
     col=col+1
    print bacteria_lst[row].bac_name.ljust(15-len(bacteria_lst[row].bac_name))+tstr + "\n"
    row=row+1
  

def make_network(year, adj_matrix, groupA, groupB):
   global pos
   #Before making the graph we have to calculate a node size
   freqs = []
   for item in groupA :
       freqs.append(item.Freq)
   for item in groupB :
       freqs.append(item.Freq)

   fmean = np.mean(freqs,axis=None)
   #print fmean

   G=nx.Graph()

   for item in groupA :
       G.add_node( item.name,size=(1000*item.Freq/(1 if fmean == 0 else fmean) ) )
   for item in groupB :
       G.add_node( item.name,size=(1000*item.Freq/(1 if fmean == 0 else fmean) ) )

   s_array = set([])
   if len(groupB) != 0 :
    for i in xrange(len(groupA)) :
       for j in xrange(len(groupB)) :
           if(adj_matrix[i][j] != -1) :
               s_array.add(adj_matrix[i][j])
               if adj_matrix[i][j] > 100 : #Red
                   G.add_edge(groupA[i].name,groupB[j].name,color='#FF0000', width=10) #Red
	       elif (adj_matrix[i][j] > 80) and (adj_matrix[i][j] <= 90) :
                   G.add_edge(groupA[i].name,groupB[j].name,color='#FF4500',width=9) #Orange Red
	       elif (adj_matrix[i][j] > 70) and (adj_matrix[i][j] <= 80) :
                   G.add_edge(groupA[i].name,groupB[j].name,color='#FF8C00',width=8) #Dark orange
	       elif (adj_matrix[i][j] > 60) and (adj_matrix[i][j] <= 70) :
                   G.add_edge(groupA[i].name,groupB[j].name,color='#FFFF00',width=7) #Yellow
	       elif (adj_matrix[i][j] > 50) and (adj_matrix[i][j] <= 60) :
                   G.add_edge(groupA[i].name,groupB[j].name,color='#9ACD32',width=6) #Yello green
	       elif (adj_matrix[i][j] > 40) and (adj_matrix[i][j] <= 50) :
                   G.add_edge(groupA[i].name,groupB[j].name,color='#7CFC00',width=5) #Lawn green
	       elif (adj_matrix[i][j] > 30) and (adj_matrix[i][j] <= 40) :
                   G.add_edge(groupA[i].name,groupB[j].name,color='#98FB98',width=4) #Pale green
	       elif (adj_matrix[i][j] > 20) and (adj_matrix[i][j] <= 30) :
                   G.add_edge(groupA[i].name,groupB[j].name,color='#ADD8E6',width=3) #Light blue
	       elif (adj_matrix[i][j] > 10) and (adj_matrix[i][j] <= 20) :
                   G.add_edge(groupA[i].name,groupB[j].name,color='#0000CD',width=2) #Medium blue
               elif (adj_matrix[i][j] > 5) and (adj_matrix[i][j] <= 10) :
                   G.add_edge(groupA[i].name,groupB[j].name,color='#00008B',width=0.5) #Dark blue
               elif (adj_matrix[i][j] <= 5) :
                   G.add_edge(groupA[i].name,groupB[j].name,color='blue',width=0)

   else :
       for i in xrange(len(groupA)) :
        for j in xrange(i) :
           if(adj_matrix[i][j] != -1) :
               s_array.add(adj_matrix[i][j])
               if adj_matrix[i][j] > 100 : #Red
                   G.add_edge(groupA[i].name,groupA[j].name,color='#FF0000', width=10) #Red
	       elif (adj_matrix[i][j] > 80) and (adj_matrix[i][j] <= 90) :
                   G.add_edge(groupA[i].name,groupA[j].name,color='#FF4500',width=9) #Orange Red
	       elif (adj_matrix[i][j] > 70) and (adj_matrix[i][j] <= 80) :
                   G.add_edge(groupA[i].name,groupA[j].name,color='#FF8C00',width=8) #Dark orange
	       elif (adj_matrix[i][j] > 60) and (adj_matrix[i][j] <= 70) :
                   G.add_edge(groupA[i].name,groupA[j].name,color='#FFFF00',width=7) #Yellow
	       elif (adj_matrix[i][j] > 50) and (adj_matrix[i][j] <= 60) :
                   G.add_edge(groupA[i].name,groupA[j].name,color='#9ACD32',width=6) #Yello green
	       elif (adj_matrix[i][j] > 40) and (adj_matrix[i][j] <= 50) :
                   G.add_edge(groupA[i].name,groupA[j].name,color='#7CFC00',width=5) #Lawn green
	       elif (adj_matrix[i][j] > 30) and (adj_matrix[i][j] <= 40) :
                   G.add_edge(groupA[i].name,groupA[j].name,color='#98FB98',width=4) #Pale green
	       elif (adj_matrix[i][j] > 20) and (adj_matrix[i][j] <= 30) :
                   G.add_edge(groupA[i].name,groupA[j].name,color='#ADD8E6',width=3) #Light blue
	       elif (adj_matrix[i][j] > 10) and (adj_matrix[i][j] <= 20) :
                   G.add_edge(groupA[i].name,groupA[j].name,color='#0000CD',width=2) #Medium blue
               elif (adj_matrix[i][j] > 5) and (adj_matrix[i][j] <= 10) :
                   G.add_edge(groupA[i].name,groupA[j].name,color='#00008B',width=0.5) #Dark blue
               elif (adj_matrix[i][j] <= 5) :
                   G.add_edge(groupA[i].name,groupA[j].name,color='blue',width=0)


   print sorted(s_array)



   nodsize = []
   for nn,dd in G.nodes_iter(data=True) :
    nodsize.append(dd['size'])

   #print nodsize
   edgewidth=[]
   for (u,v,d) in G.edges(data=True):
        edgewidth.append(G.get_edge_data(u,v)['width'])
        #print G.get_edge_data(u,v)

   edgecolor=[]
   for (u,v,d) in G.edges(data=True):
        edgecolor.append(G.get_edge_data(u,v)['color'])


   if len(pos) == 0 :
        pos=nx.graphviz_layout(G)

   pos_lbl = dict() #pos
   for nn,dd in G.nodes_iter(data=True) :
      if dd['size'] == 0 :
        pos_lbl[nn] = [-100,-100]
      else :
        pos_lbl[nn] = pos[nn]


   #a_matrix = []
   #for b in bacteria_lst :
   #    b.Freq = 0

   print pos_lbl
   #plt.rcParams['text.usetex'] = False
   nx.draw_networkx_nodes(G,pos, node_size=nodsize, node_color='grey')
   nx.draw_networkx_edges(G,pos,width = edgewidth, edge_color = edgecolor)
   nx.draw_networkx_labels(G, pos_lbl,fontsize=16, font_color='black', font_weight='bold')

   plt.axis('off')
   plt.title(year)
   plt.savefig(year+".pdf")

   plt.show()

   

def print_total_freqs() :
    for i in range(n) :
        print bacteria_lst[i].bac_name + ": " + str(bacteria_lst[i].Freq)




def make_venn_diagram() :
    plt.figure(figsize=(10,10))
    v = venn3(subsets=(25, 50, 12, 76, 6, 10, 1 ), set_labels = ('iners', 'crispatus', 'gasseri', 'D'))
   # v.get_patch_by_id('iners').set_alpha(1.0)
   # v.get_patch_by_id('iners').set_color('white')
   # v.get_label_by_id('iners').set_text('Unknown')
    c = venn3_circles(subsets=(25, 50, 12, 76, 6, 10, 1), linestyle='dashed')
    c[0].set_lw(1.0)
    c[0].set_ls('dotted')
    plt.title("Sample Venn diagram")
    #plt.annotate('Unknown set', xy=v.get_label_by_id('100').get_position() - np.array([0, 0.05]), xytext=(-70,-70),
    #            ha='center', textcoords='offset points', bbox=dict(boxstyle='round,pad=0.5', fc='gray', alpha=0.1),
    #            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5',color='gray'))

    plt.axis('off')
    plt.show()

def make_bacteria_dict2(query_filename):
    global bacteria_lst
    file = open(query_filename)
    query_string = ""
    while 1:
      line = file.readline()
      if not line:
        break
      if line[:9] == "query_str" :
          if line[len(line)-1] == "\n" :
            line = line[:-1]
          query_string +=line
          break
      
    query_string = query_string[13:len(query_string)-1]
    query_string.strip()

    temp_list =  query_string.split("[All Fields]")
    tmp_list = []
    for item in temp_list :
        tmp_list.append(item.replace('OR','').replace('AND','').strip())

    tmp_list = set(tmp_list)
    for item in tmp_list :
        if item == '' :
            continue
        bnode = bacteria.BacteriaNode()
        bnode.bac_name = item
        bacteria_lst.append( bnode )
        global n
        n+=1

    #print bacteria_lst
    print "Given query string: ", query_string



def main(argv):

   flag_1 = False #Co-occurrence of any of the words in a group with other words in the same group excluding themselves
   flag_2 = False #Co-occurrence of any of the words in Group 1 with any of the words in Group 2
   flag_kw = False #Keyword approach
   flag_tm = False #Timing approach
   group_1_filename = group_2_filename = kw_filename = tm_filename = ""

   #Parsing command line arguments:
   try:
      opts, args = getopt.getopt(argv[1:],"1:2:3",['kw=', "tm="])
      #print opts
      #print args
   except getopt.GetoptError:
      print "pubmed.py <parameters>"
      sys.exit(2)
   for opt, arg in opts:
      if opt == "-1":
        flag_1 = True
        group_1_filename = arg
      elif opt == "-2" :
        flag_2 = True
        group_2_filename = arg
      elif opt in ("--kw") :
        flag_kw = True
        kw_filename = arg
      elif opt == "--tm" :
        flag_tm = True
        tm_filename = arg


   if (flag_1 == True) and (flag_2 == False) and (flag_kw == False) and (flag_tm == False) :
        print 'Co-occurrence of any of the words in a group with other words in the same group excluding themselves'
        read_abstracts_from_xml("pubmed_result.xml")
        group = []
        group = read_txt_file(group_1_filename)
        adj_matrix = []
        adj_matrix = make_adj_matrix1(group)
        print_adj_matrix_to_csv1(group, adj_matrix, 'adj_matrix_11.csv')
        sys.exit()
   elif (flag_1 == True) and (flag_2 == True) and (flag_kw == False) and (flag_tm == False) :
        print 'Co-occurrence of any of the words in Group 1 with any of the words in Group 2'
        read_abstracts_from_xml("pubmed_result.xml")
        group1 = []
        group2 = []
        group1 = read_txt_file(group_1_filename)
        group2 = read_txt_file(group_2_filename)
        adj_matrix = []
        adj_matrix = make_adj_matrix2(group1, group2)
        print_adj_matrix_to_csv2(group1, group2, adj_matrix, 'adj_matrix_12.csv')
        sys.exit()
   elif (flag_1 == False) and (flag_2 == False) and (flag_kw == True) and (flag_tm == False) :
        print "Keyword approach..."
        make_kw_approach(kw_filename)
        sys.exit()
   elif (flag_1 == False) and (flag_2 == False) and (flag_kw == False) and (flag_tm == True) :
        print 'Approach Time was choosen'
        make_time_layer(tm_filename)
        sys.exit()
           
         
   
def make_kw_approach(filename):
    #Load abstracts
    print "Reading data file..."
    read_abstracts_from_xml("pubmed_result.xml")
    global abstracts

    bacteria_list = []
    bacteria_list = read_txt_file(filename)
    i=0
    for abstract in abstracts :
        kwe.make_keyword_candidates(abstract.AbstractText)
        kwe.make_cooccurrence_matrix()
        abstract.key_words = kwe.make_keywords_list()
        #print i
        #print abstract.key_words
        #Tie bacteria & abstracts
        #Tie keywords to bacteria: key_word<abstract_id, abstract_id, ...>
        for bacteria in bacteria_list :
            if abstract.AbstractText.rfind( bacteria.name ) != -1 :
                #print bacteria.name
                #print abstract.AbstractText
                bacteria.Freq += 1
                for keyword in abstract.key_words :
                    try :
                        bacteria.key_words[keyword].append(abstract.id)
                    except :
                        bacteria.key_words[keyword] = []
                        bacteria.key_words[keyword].append(abstract.id)
            
            
        #i+=1
        #if i == 2 : break

    print "Done with extraction keywords"
    
    #for bacteria in bacteria_list :
    #    print bacteria.name
    #    print bacteria.key_words
    #Adjacency matric, strong connections
    adj_matrix = []
    for i in xrange(len(bacteria_list)):
        adj_matrix.append([])
        for j in xrange(len(bacteria_list)):
            adj_matrix[i].append(0)

    for i in xrange( len(bacteria_list) ) :
        for j in xrange( (i+1), len(bacteria_list) ) :
            for kw in bacteria_list[i].key_words :
                for kww in bacteria_list[j].key_words :
                    if kw == kww :
                        skw = set()
                        skw = set(list(kw))
                        skww = set()
                        skww = set(list(skww))
                        if len(skw.symmetric_difference(skww)) > 0 :
                            adj_matrix[i][j] += 1

    print_adj_matrix_to_csv1(bacteria_list, adj_matrix, 'adj_matrix_strong.csv')

    for bacteria in bacteria_list :
        with open(str(bacteria.name)+".csv", 'wb') as csvfile :
            spamwriter = csv.writer(csvfile)
            #print bacteria.name
            for item in bacteria.key_words :
                spamwriter.writerow( str(item) )

    
def make_time_layer(filename):
    global abstracts
    read_abstracts_from_xml("pubmed_result.xml")
    tl.make_bacteria_dict(filename)
    PubYears = dict()
    PubYears = tl.extract_publication_years(abstracts)
    min_year = min(PubYears)
    print min_year
    for year in PubYears :
       #print year[0]
       tl.make_adj_matrix(abstracts, year[0])
       #tl.print_adj_matrix()
       tl.make_time_network(year[0])
            

def read_abstracts_from_xml(filename):
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
       if len(PubmedArticle.getElementsByTagName('Author')) == 0 :
           AuthorList = "NA"
       else :
           for Author in PubmedArticle.getElementsByTagName('Author') :
              try :
                AuthorList += Author.getElementsByTagName('LastName')[0].firstChild.nodeValue.encode('utf-8') + ", "
              except :
                AuthorList += "NA"
                
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
       abstract.id = index
       abstracts.append(abstract)
       index += 1
       #print len(abstracts)



def make_adj_matrix2(GroupA, GroupB) :
  adj_matrix = []
  for i in xrange(len(GroupA)):
    adj_matrix.append([])
    for j in xrange(len(GroupB)):
      adj_matrix[i].append(0)
  #print n
  for z in xrange(len(abstracts)) :
    for i in xrange(len(GroupA)) :
        if abstracts[z].AbstractText.rfind( GroupA[i].name ) != -1 :
          GroupA[i].Freq += 1
          GroupA[i].abstract_indexes.append(abstracts[z].id)
          for j in xrange(len(GroupB)) :
            if  abstracts[z].AbstractText.rfind( GroupB[j].name ) != -1   :
                adj_matrix[i][j]+=1
                GroupB[j].Freq += 1
          #continue

  return adj_matrix #, GroupA, GroupB

def make_adj_matrix1(group) :
  """
  Looks for co-occurrence of the words in the given group with themselves
  """
  n = len(group)
  adj_matrix = []
  for i in xrange(n):
    adj_matrix.append([])
    for j in xrange(n):
      adj_matrix[i].append(0)

  #For each abstract in extracted abstract set:
  for z in xrange(len(abstracts)) :
    for i in xrange(n) :
        if abstracts[z].AbstractText.rfind( group[i].name ) != -1 :
          group[i].Freq += 1
          group[i].abstract_indexes.append(abstracts[z].id)
          for j in xrange(n) :
            if ( abstracts[z].AbstractText.rfind( group[j].name ) != -1 ) and (i != j)  :
                adj_matrix[i][j]+=1
                group[j].Freq += 1
          #continue

  return adj_matrix #, GroupA, GroupB


def print_adj_matrix_to_csv2(group1, group2, adj_matrix, filemane) :
    #print len(group1)
    #print len(group2)
    #print len(adj_matrix)
    with open(filemane, 'wb') as csvfile :
        spamwriter = csv.writer(csvfile, delimiter=',')
        tarr = []
        #Writing a header:
        tarr.append(' ')
        for item in group2 :
            tarr.append(item.name)
        for item in group1 :
            tarr.append(item.name)
        spamwriter.writerow(tarr)
        #print tarr
        #Writing rows:
        for i in xrange(len(group1)+len(group2)) :
           tarr = []
           if i >= len(group2) :
               tarr.append( group1[i-len(group2)].name )
           else :
               tarr.append(group2[i].name)

           for j in xrange(len(group1)+len(group2)) :
                if ( j < len(group2) ) and ( i >= len(group2) ):
                    tarr.append( adj_matrix[i-len(group2)][j] )
                else :
                    tarr.append(0)
           
           spamwriter.writerow( tarr )
        
def print_adj_matrix_to_csv1(group, adj_matrix, filemane) :
    with open(filemane, 'wb') as csvfile :
        spamwriter = csv.writer(csvfile, delimiter=',')
        tarr = []
        #Writing a header:
        tarr.append(' ')
        for item in group :
            tarr.append(item.name)

        spamwriter.writerow(tarr)
        #print tarr
        #Writing rows:
        for i in xrange(len(group)) :
           tarr = []
           tarr.append(group[i].name)
           for j in xrange( len(group) ) :
                tarr.append( adj_matrix[i][j] )
                
           spamwriter.writerow( tarr )



if __name__ == "__main__":
   main(sys.argv)
