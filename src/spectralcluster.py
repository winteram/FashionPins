import numpy as np
from sklearn import cluster
import collections
import pprint

correlations = np.genfromtxt('/Users/pinarozturk/Documents/LastFm/cosdicteach100.csv', delimiter=',')
#correlations = np.genfromtxt('../data/cosdicteach100.csv', delimiter=',')
#print correlations.shape
#print correlations

symbol_dict=collections.OrderedDict()
headers = correlations[0,:] [1:]

correlations = np.delete(correlations, (0), axis=0)#delete first row - CosMat has boardids in 1st row
correlations = np.delete(correlations,(0), axis=1)#delete first column - CosMat has boardids in 1st col
#print correlations
#print correlations.shape

i=0
for item in headers[::-1]:
    i+=1
    key=i
    symbol_dict[key]=str(item)
#print symbol_dict
symbols, names = np.array(symbol_dict.items()).T

def test(correlations,itemnum):
    correlations = np.delete(correlations, (itemnum), axis=0)#delete first row - CosMat has boardids in 1st row
    correlations = np.delete(correlations,(itemnum), axis=1)#delete first column - CosMat has boardids in 1st col
    #print correlations
    #print correlations.shape
    del symbol_dict[itemnum]
    #print symbol_dict
    symbols, names = np.array(symbol_dict.items()).T
    return correlations,names

def affinityprop(correlations,names):
    n_clusters=0
    a,labels = cluster.affinity_propagation(correlations)
    #print labels
    print "Affinity Propagation Clusters"
    for i in range(labels.max()+1):
        print 'Cluster %i: %s' % ((i+1),
                              ', '.join(names[labels==i]))
        if len(names[labels==i]) > 1:
            n_clusters+=1
    print "Number of Clusters with more than 1 element: " + str(n_clusters)
    return n_clusters
    
def spectralcluster(correlations,n_clusters,names):
    labels=cluster.spectral_clustering(correlations,n_clusters=n_clusters, eigen_solver=None, random_state=0, n_init=10,  k=None, eigen_tol=0.0, 
    assign_labels='kmeans', mode=None)
    #print labels
    clusdict=[]
    print ""
    print "Spectral Clustering - shape: " + str(correlations.shape)
    for i in range(labels.max()+1):
        print 'Cluster %i: %s' % ((i+1),', '.join(names[labels==i]))
        clusdict.append(names[labels==i])
    #print clusdict                     
    return clusdict


n_clusters=affinityprop(correlations,names)+1
#n_clusters=10

clusdict1=spectralcluster(correlations,n_clusters,names)


correlations,names=test(correlations,73) # Test for cluster stability - remove item/check clusters
clusdict2=spectralcluster(correlations,n_clusters,names)

def intersectunion(val1,val2):
    # Find intersection of first board sources & second board sources
    a,b=set(val1), set(val2)
    intersect= len(a.intersection(b))
    #print "intersect: " + str(intersect)
    #print a & b
    union=len(val1)+len(val2)-intersect
    #print "Union: " + str(union)
    return intersect,union
    #return True
    
  
def compareLCS(clusdict1,clusdict2):
    intersecta=[]
    cchange=[]    
    for i in range(0,n_clusters):
        for y in range(0,n_clusters):
            val1=clusdict1[i]
            val2=clusdict2[y]
            intersect,union=intersectunion(val1,val2)
            intersecta.append(["Clusdict1 C"+str(i+1),"Clusdict2 C" + str(y+1),union,intersect])
    #print len(intersecta)
    indices=[]
    for a in range(0,n_clusters):
        indices=[]
        for b in range(len(intersecta)):
            if intersecta[b][0] == "Clusdict1 C" + str(a+1):
                #print intersecta[b][0]
                indices.append(intersecta[b])
        cchange.append(max(indices, key=lambda x: x[3]))
           
    print ""
    print "Cluster Change - Intersect & Union"
    pprint.pprint(cchange)
    return True
     
compareLCS(clusdict1,clusdict2)

