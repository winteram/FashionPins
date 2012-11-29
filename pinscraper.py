import urllib
import re
from bs4 import BeautifulSoup
import math
import time
import pprint
import csv

searchword="fashion"
pinurl = "http://pinterest.com"
boardpgurl = "http://pinterest.com/search/boards/?q="+searchword+"&page="


# initialize arrays
boardlist=[]
pinids = []
boards = []
sources = []
userids = []

start = time.time()
# test whether more than 0.5 second has passed
elapsed = time.time() - start
if elapsed > 0.5:
    time.sleep(0.5)

start = time.time()

nboardpages=3
for bpage in range(1,nboardpages):
    print "opening board list " + str(bpage)
    boardpg = urllib.urlopen(boardpgurl+str(bpage))
    boardread = boardpg.read()
    soup = BeautifulSoup(boardread)
    for board_div in soup.find_all("div","pin pinBoard"):
        for h3_name in board_div("h3","serif"):
            for a_name in h3_name("a"):
                board_name=a_name['href']
                boardlist.append(board_name)

print "Number of boards: "+str(len(boardlist))

for a in range(0,len(boardlist)):
	firstpg = urllib.urlopen(pinurl + "/" + boardlist[a])
	pageread = firstpg.read()
	count = re.compile(ur'<strong>(.*?)</strong> pins', re.UNICODE)
	pincount = count.search(pageread).group(1)
	npages = math.ceil(int(re.sub(r'[^\d-]+','',pincount))/50)
	print "Pin pages in board "+str(a)+": "+str(npages)
	npage=int(npages)			
   	for i in range(1,npage+2):
    		pages=urllib.urlopen(pinurl+"/"+boardlist[a]+"?page="+str(i))
    		page=pages.read()
    		soup = BeautifulSoup(page)
    		for pin in soup.find_all("div","pin"):
    	   		pinid = "None"
    	   		board = "None"
    	  	 	source = "None"
                        userid = "None"
                        for userid_a in pin.find_all("h4","user"):
                            userid = userid_a[0]["href"]
           		for pinid_a in pin.find_all("a","PinImage ImgLink"):
               			pinid = pinid_a['href']
           		for clearfix in pin.find_all("div","convo attribution clearfix"):
                   		for link in clearfix.find_all("a"):
                       	   		board=boardlist[a]
                           		source = link['href']
           		pinids.append(pinid)
           		boards.append(board)
           		sources.append(source)
                        userids.append(userid)


print "pinids: " + str(len(pinids))
print "boards: " + str(len(boards))
print "sources: " + str(len(sources))
print "users: " + str(len(userids))

allpins = zip(pinids,userids,boards,sources)
f = open("allpins.txt","w")
writer = csv.writer(f)
writer.writerows(allpins)
f.close()
