from pandas import DataFrame
from collections import Counter
import csv
# open updated testpins (sources pinned more than twice)
f=open('testpins2.csv','rb')
reader=csv.reader(f)
headers=reader.next()
headers
column = {}
for h in headers:
	column[h] = []

for row in reader:
	for h, v in zip(headers, row):
		column[h].append(v)

# Find unique sources and users
c=Counter(column['source'])
d=Counter(column['user'])

#Create a dict of user+source 
pdict={}
for a in range(len(column['source'])):
	key=column['user'][a]+column['source'][a]
	if key not in pdict:
		pdict[key]=1

i=0
y=0
pin={}
#Check whether a user+source combo exists in dict
for i in range(0,len(c)):
	pin[list(c)[i]]={}
	for y in range(len(d)):
		key2=list(d)[y]+list(c)[i]
		if key2 in pdict:
			pin[list(c)[i]][list(d)[y]]=1
		else:
			pin[list(c)[i]][list(d)[y]]=0

df = DataFrame(pin)
df.to_csv('simmat.csv')
