import numpy as np
from sklearn import cluster
import collections
import pprint

correlations = np.genfromtxt('/Users/pinarozturk/Documents/LastFm/cosdicteach100.csv', delimiter=',')
#correlations = np.genfromtxt('../data/cosdicteach75.csv', delimiter=',')

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
    clusdict={}
    print ""
    print "Spectral Clustering - shape: " + str(correlations.shape)
    for i in range(labels.max()+1):
        print 'Cluster %i: %s' % ((i+1),', '.join(names[labels==i]))
        key=(str(names[labels==i]))
        clusdict[key]=i+1
    #print clusdict                     
    return clusdict


n_clusters=affinityprop(correlations,names)+1
#n_clusters=10

clusdict1=spectralcluster(correlations,n_clusters,names)

correlations,names=test(correlations,73) # Test for cluster stability - remove item/check clusters
clusdict2=spectralcluster(correlations,n_clusters,names)
    
#Compare and match clusters - Find longest common substring
def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]

def compareLCS(clusdict1,clusdict2):
    LCS=[]
    LCS2=[]    
    for i in range(1,n_clusters+1):
        for y in range(1,n_clusters+1):
            val1=clusdict1.keys()[clusdict1.values().index(i)]
            val2=clusdict2.keys()[clusdict2.values().index(y)]
            LCS.append("Clusdict1 C"+str(i) +'-' + "Clusdict2 C" + str(y) + '-'+ longest_common_substring(val1,val2))
        LCS2.append(max(LCS, key=len))
        LCS=[]
    print ""
    print "Cluster Longest Common Substring"
    pprint.pprint(LCS2)
    return True
    
compareLCS(clusdict1,clusdict2)

