import urllib
import re
from bs4 import BeautifulSoup
import math
import time
import pprint
from unicoderw import UnicodeWriter

searchword="fashion"
pinurl = "http://pinterest.com"
boardpgurl = "http://pinterest.com/search/boards/?q="+searchword+"&page="


# initialize arrays
boardlist=[]
pinids = []
boards = []
sources = []
userlist = []
userids = []

start = time.time()

nboardpages=3
for bpage in range(1,nboardpages):
    print "opening board list " + str(bpage)
    boardpg = urllib.urlopen(boardpgurl+str(bpage))
    # test whether more than 0.5 second has passed
    elapsed = time.time() - start
    if elapsed > 0.5:
        time.sleep(0.5)
    start = time.time()

    boardread = boardpg.read()
    soup = BeautifulSoup(boardread)
    for board_div in soup.find_all("div","pin pinBoard"):
        for userid_a in board_div.find_all("a","colorless"):
            userid = userid_a["href"]
            userlist.append(userid)
        for h3_name in board_div("h3","serif"):
            for a_name in h3_name("a"):
                board_name=a_name['href']
                boardlist.append(board_name)

print "Number of boards: "+str(len(boardlist))

for a in range(0,len(boardlist)):
    firstpg = urllib.urlopen(pinurl + "/" + boardlist[a])
    # test whether more than 0.5 second has passed
    elapsed = time.time() - start
    if elapsed > 0.5:
        time.sleep(0.5)
    start = time.time()

    pageread = firstpg.read()
    count = re.compile(ur'<strong>(.*?)</strong> pins', re.UNICODE)
#     numpinsrch = count.search(pageread).groups()
#     print "Number of pins on page: " + ".".join(numpinsrch)
#     pincount = str(numpinsrch)
#     npages = math.ceil(int(re.sub(r'[^\d-]+','',pincount))/50)
    pincntpage = count.search(pageread)
    if pincntpage:
        pincount = count.search(pageread).groups()
    else:
        print "Error with finding # pins: " + boardlist[a]
    print "Number of pins on page: " + str(pincount)
    npages = math.ceil(float(re.sub(r'[^\d-]+','',pincount[0]))/50)
    print "Pin pages in board "+str(a)+": "+str(npages)
    npage=int(npages)			
    for i in range(1,npage+2):
        pages=urllib.urlopen(pinurl+"/"+boardlist[a]+"?page="+str(i))
        # test whether more than 0.5 second has passed
        elapsed = time.time() - start
        if elapsed > 0.5:
            time.sleep(0.5)
        start = time.time()

        page=pages.read()
        soup = BeautifulSoup(page)
        for pin in soup.find_all("div","pin"):
            pinid = "None"
            board = "None"
            source = "None"
            userid = "None"
            for pinid_a in pin.find_all("a","PinImage ImgLink"):
                pinid = pinid_a['href']
            for clearfix in pin.find_all("div","convo attribution clearfix"):
                for link in clearfix.find_all("a"):
                    userid=userlist[a]
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
writer = UnicodeWriter(f)
writer.writerows(allpins)
f.close()
