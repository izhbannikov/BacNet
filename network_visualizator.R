setwd("~/Dropbox/cs576_project/BacNet/")
library(igraph)

group<-read.csv("GroupC.txt", header = F)
network_data<-read.csv("adj_matrix_12.csv", header = T, stringsAsFactors=F, sep=",")
network_data <- network_data[,2:ncol(network_data)]
names(network_data)
bsk.network<-graph.adjacency( ceiling(network_data) )

#Subset the data. If we want to exclude nodes who are in the network only tangentially 
#(participate in one or two relationships only)
# we can exclude the by subsetting the graph on the basis of the 'degree':
bad.vs<-V(bsk.network)[degree(bsk.network)<3] #identify those vertices part of less than three edges
bsk.network<-delete.vertices(bsk.network, bad.vs) #exclude them from the graph
# Plot the data.Some details about the graph can be specified in advance.
# For example we can separate some vertices (people) by color:
#useful for highlighting certain nodes.
#Works by matching the name attribute of the vertex to the one specified in the 'ifelse' expression
V(bsk.network)$color<-ifelse(V(bsk.network)$name %in% group$V1, 'blue', 'red') 
# We can also color the connecting edges differently depending on the 'grade': 
E(bsk.network)$color<-ifelse(E(bsk.network)$grade<=50, "red", "grey")

# or depending on the different specialization ('spec'):

E(bsk.network)$color<-ifelse(E(bsk.network)$spec=='X', "red", ifelse(E(bsk.network)$spec=='Y', "blue", "grey"))

# Note: the example uses nested ifelse expressions which is in general a bad idea but does the job in this case
# Additional attributes like size can be further specified in an analogous manner, either in advance or when the plot function is called:

V(bsk.network)$size<-degree(bsk.network)/10#here the size of the vertices is specified by the degree of the vertex, so that people supervising more have get proportionally bigger dots. Getting the right scale gets some playing around with the parameters of the scale function (from the 'base' package)

# Note that if the same attribute is specified beforehand and inside the function, the former will be overridden.
# And finally the plot itself:
par(mai=c(0,0,1,0))   		#this specifies the size of the margins. the default settings leave too much free space on all sides (if no axes are printed)
plot(bsk.network,				#the graph to be plotted
     layout=layout.fruchterman.reingold(bsk.network, repulserad=20),	# the layout method. see the igraph documentation for details
     main='Co-occurrence with any of the word in Group C with any of the word in Group B',	#specifies the title
     edge.arrow.width = 0,
     vertex.label.dist=0.5,			#puts the name labels slightly off the dots
     vertex.frame.color='blue', 		#the color of the border of the dots 
     vertex.label.color='black',		#the color of the name labels
     vertex.label.font=2,			#the font of the name labels
     vertex.label=V(bsk.network)$name,		#specifies the lables of the vertices. in this case the 'name' attribute is used
     vertex.label.cex=1			#specifies the size of the font of the labels. can also be made to vary
)



#plot(bsk.network,layout=layout.kamada.kawai(bsk.network, kkconst = 300),edge.arrow.width = 0, vertex.label.dist=0.5,vertex.frame.color='blue',vertex.label.color='black', vertex.label.font=1, vertex.label=V(bsk.network)$name)
#plot(bsk.network,layout=layout.fruchterman.reingold(bsk.network, repulserad=10),edge.arrow.width = 0, vertex.label.dist=0,vertex.frame.color='blue',vertex.label.color='black', vertex.label.font=1, vertex.label=V(bsk.network)$name)
#title(main="Co-occurrence with any of the word in Group 2 with any of the word in Group 2 (excluding themselves)")
#title(main="Co-occurrence with any of the word in Group 3 with any of the word in Group 2")
