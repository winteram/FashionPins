import csv
f=open('testpins.csv','rb')
reader=csv.reader(f)
headers=reader.next()
headers
column = {}
for h in headers:
	column[h] = []

for row in reader:
	for h, v in zip(headers, row):
		column[h].append(v)

from collections import Counter
c=Counter(column['source'])
d=Counter(column['user'])
print "Number of Unique Users: " + str(len(d))
print "Number of Unique Sources: " + str(len(c))
print "Number of Sources Pinned only once: "+ str(len([i for i in c if c[i]==1]))
print "Number of Sources Pinned twice: "+ str(len([i for i in c if c[i]==2]))
print "Number of Sources Pinned more than 2times: "+ str(len([i for i in c if c[i]>2]))
print c.most_common(10)
fw=open("frequency.csv","w")
writer=csv.writer(fw)
writer.writerows(c.items())
fw.close()
