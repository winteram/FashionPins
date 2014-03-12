# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

fw = open('fashion_sim_edgelist.ncol','w')
fh = open('winteram_fashion_sim_2526.csv','r')
fh.readline()
for line in fh:
    fbid_r, fbid_c, j_sim = line.strip().split(',')
    if float(j_sim)>0:
        row = fbid_r+'\t'+fbid_c+'\t'+j_sim+'\n'
        fw.write(row)
fh.close()
fw.close()

# <codecell>

import igraph as ig
import numpy as np
from collections import Counter
import json

# <codecell>

fcig = ig.read('fashion_sim_edgelist.ncol')

# <codecell>

fc = fcig.as_undirected(combine_edges="max")

# <codecell>

np.mean(fc.degree())

# <codecell>

np.mean(fc.es["weight"])

# <codecell>

clig = fc.community_fastgreedy(weights="weight")

# <codecell>

cl = clig.as_clustering()

# <codecell>

Counter(cl.membership)

# <codecell>

cllabs = cl.membership

# <codecell>

nodes = []
links = []

# <codecell>

i = 0
for v in fc.vs:
    v_dict = {"name":v["name"],"group":cllabs[i]}
    nodes.append(v_dict)
    i += 1

# <codecell>

for e in fc.es:
    l_dict = {"source":fc.vs[e.source]["name"],"target":fc.vs[e.target]["name"],"value":e["weight"]}
    links.append(l_dict)

# <codecell>

G = {"nodes":nodes,"links":links}

# <codecell>

fp = open('fashion_pages.json','w')
json.dump(G,fp)
fp.close()

# <codecell>


