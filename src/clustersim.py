import csv
import collections
import numpy as np
from pandas import DataFrame

df = 

# Note: control for users in similarity across boards, or measure similarity at user level

# Possible clustering algorithms:
#   k-NN
#   Spectral clustering
#   PCA
# 
# Cluster validation:
#  - Check whether held-out items changes the cluster assignment of non-held out items after being added
#  - 1. Hold out items, 
# 	 2. Calculate similarity, 
# 	 3. Do clustering, 
# 	 4. See if held-out items are pinned by users in same cluster
#
# Metrics for evaluation:
#   F-measure
#   AUC
#   Rand index