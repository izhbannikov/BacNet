#!/usr/bin/env python
import bacteria
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

__author__="ilya"
__date__ ="$08.11.2012 10:53:27$"

PubYears = dict()

a_matrix = []
a_matrix_words = []
bacteria_lst = []
n = 0
abstracts = []
pos = []


def make_bacteria_dict(filename):    # write Fibonacci series up to n
    global bacteria_lst
    file = open(filename)
    while 1:
      line = file.readline()
      if not line:
        break
      bnode = bacteria.BacteriaNode()
      bnode.bac_name = line.strip()
      bacteria_lst.append( bnode )
      global n
      n+=1
      
    return bacteria_lst
    
def make_adj_matrix(_abstracts, ToYear) :
    global abstracts
    abstracts = _abstracts
    for i in xrange(n):
        a_matrix.append([])
        for j in xrange(n):
            a_matrix[i].append(0)

    #print PubYears
    for pub_year in PubYears :
        if str(pub_year[0]) <= ToYear :
            make_adj_matrix_by_year(str(pub_year[0]), pub_year[1])

    #for b in bacteria_lst :
    #    print b.bac_name + " " + str(b.Freq)
        
def extract_publication_years(abstracts):
    global PubYears
    tmp_pub_years = dict()
    for abstract in abstracts :
        #print abstract.AbstractText
        if str(abstract.Year) != '1900' :
            tmp_pub_years[str(abstract.Year)] = 0

    for abstract in abstracts :
        if str(abstract.Year) != '1900' :
            tmp_pub_years[str(abstract.Year)] += 1

    PubYears = sorted(tmp_pub_years.iteritems())

    return PubYears

def calculate_trend(year):
    #Trend is calculated for 3 last years
    #Number of puplications(bacteria frequency)/Total publications per year
    for bacteria in bacteria_lst :
        prev_trend_value = bacteria.trend[0]
        years_sampled = len( bacteria.trend )
        if years_sampled > 3 :
            for i in bacteria.trend :
                if prev_trend_value > i :
                    trend_indicator = 'UP'
        else :
            bacteria.trend_indicator = 'NA'


def make_adj_matrix_by_year(year, total_num_publ) :
  #print year
  global a_matrix
  global abstracts
  global PubYears
  #print len(abstracts)
  for i in xrange(n) :
    for z in xrange(len(abstracts)) :
      if ( (abstracts[z].AbstractText.rfind( bacteria_lst[i].bac_name )) != -1 ) and (abstracts[z].Year == year) :
        bacteria_lst[i].Freq += 1
        bacteria_lst[i].abstract_ids.append( abstracts[z].id )
        for j in xrange(n) :
            if ((abstracts[z].AbstractText.rfind( bacteria_lst[j].bac_name) != -1)  and (abstracts[z].Year == year))  :
                a_matrix[i][j]+=1
                continue #next bacteria name
    bacteria_lst[i].trend.append( bacteria_lst[i].Freq/total_num_publ )
    
    


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

def make_time_network(year):
   global a_matrix
   global pos
   #Before making the graph we have to calculate a node size
   freqs = []
   for b in xrange(n) :
       freqs.append(bacteria_lst[b].Freq)

   fmean = np.mean(freqs,axis=None)
   #print fmean

   G=nx.Graph()

   for b in xrange(n) :
       #if (bacteria_lst[b].Freq < 15) :
       # G.add_node( bacteria_lst[b].bac_name,size=( 6000*bacteria_lst[b].Freq/(1 if fmean == 0 else fmean) ) )
       #elif (bacteria_lst[b].Freq >= 15) :
       G.add_node( bacteria_lst[b].bac_name,size=(1000*bacteria_lst[b].Freq/(1 if fmean == 0 else fmean) ) )

   s_array = set([])
   for i in xrange(n) :
       for j in xrange(i) :
           if(a_matrix[i][j] != -1) :
               s_array.add(a_matrix[i][j])
               if a_matrix[i][j] > 100 : #Red
                   G.add_edge(bacteria_lst[i].bac_name,bacteria_lst[j].bac_name,color='#FF0000', width=10) #Red
	       elif (a_matrix[i][j] > 80) and (a_matrix[i][j] <= 90) :
                   G.add_edge(bacteria_lst[i].bac_name,bacteria_lst[j].bac_name,color='#FF4500',width=9) #Orange Red
	       elif (a_matrix[i][j] > 70) and (a_matrix[i][j] <= 80) :
                   G.add_edge(bacteria_lst[i].bac_name,bacteria_lst[j].bac_name,color='#FF8C00',width=8) #Dark orange
	       elif (a_matrix[i][j] > 60) and (a_matrix[i][j] <= 70) :
                   G.add_edge(bacteria_lst[i].bac_name,bacteria_lst[j].bac_name,color='#FFFF00',width=7) #Yellow
	       elif (a_matrix[i][j] > 50) and (a_matrix[i][j] <= 60) :
                   G.add_edge(bacteria_lst[i].bac_name,bacteria_lst[j].bac_name,color='#9ACD32',width=6) #Yello green
	       elif (a_matrix[i][j] > 40) and (a_matrix[i][j] <= 50) :
                   G.add_edge(bacteria_lst[i].bac_name,bacteria_lst[j].bac_name,color='#7CFC00',width=5) #Lawn green
	       elif (a_matrix[i][j] > 30) and (a_matrix[i][j] <= 40) :
                   G.add_edge(bacteria_lst[i].bac_name,bacteria_lst[j].bac_name,color='#98FB98',width=4) #Pale green
	       elif (a_matrix[i][j] > 20) and (a_matrix[i][j] <= 30) :
                   G.add_edge(bacteria_lst[i].bac_name,bacteria_lst[j].bac_name,color='#ADD8E6',width=3) #Light blue
	       elif (a_matrix[i][j] > 10) and (a_matrix[i][j] <= 20) :
                   G.add_edge(bacteria_lst[i].bac_name,bacteria_lst[j].bac_name,color='#0000CD',width=2) #Medium blue
               elif (a_matrix[i][j] > 5) and (a_matrix[i][j] <= 10) :
                   G.add_edge(bacteria_lst[i].bac_name,bacteria_lst[j].bac_name,color='#00008B',width=0.5) #Dark blue
               elif (a_matrix[i][j] <= 5) :
                   G.add_edge(bacteria_lst[i].bac_name,bacteria_lst[j].bac_name,color='blue',width=0)


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
        
   
   a_matrix = []
   for b in bacteria_lst :
       b.Freq = 0

   #print pos_lbl
   #plt.rcParams['text.usetex'] = False
   nx.draw_networkx_nodes(G,pos, node_size=nodsize, node_color='grey')
   nx.draw_networkx_edges(G,pos,width = edgewidth, edge_color = edgecolor)
   nx.draw_networkx_labels(G, pos_lbl,fontsize=16, font_color='black', font_weight='bold')
   
   plt.axis('off')
   plt.title(year)
   plt.savefig(year+".pdf")

   #plt.show()


