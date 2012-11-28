setwd("~/BacNet/")
library(igraph)

network_data<-read.csv("adj_matrix_12.csv", header = T, stringsAsFactors=F, sep=",")
network_data <- network_data[,2:ncol(network_data)]
names(network_data)

bsk.network<-graph.adjacency( network_data )
#plot(bsk.network,layout=layout.kamada.kawai(bsk.network, kkconst = 300),edge.arrow.width = 0, vertex.label.dist=0.5,vertex.frame.color='blue',vertex.label.color='black', vertex.label.font=1, vertex.label=V(bsk.network)$name)
plot(bsk.network,layout=layout.fruchterman.reingold(bsk.network, repulserad=10),edge.arrow.width = 0, vertex.label.dist=0,vertex.frame.color='blue',vertex.label.color='black', vertex.label.font=1, vertex.label=V(bsk.network)$name)
