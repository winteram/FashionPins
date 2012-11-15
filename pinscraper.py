import urllib
import re
from bs4 import BeautifulSoup
import math
import time
import pprint

user = "calistoddard"
pinurl = "http://pinterest.com"
pp = pprint.PrettyPrinter(indent=4)

firstpg = urllib.urlopen(pinurl + "/" + user + "/pins/?page=3")
page = firstpg.read()
fh = open("calliepins.html","w")
fh.write(page)
fh.close()
 
# initialize arrays
pinids = []
boards = []
sources = []

count = re.compile(ur'<strong>(.*?)</strong> Pins', re.UNICODE)
pincount = count.search(page).group(1)
npages = math.ceil(int(re.sub(r'[^\d-]+','',pincount))/50)
npages

start = time.time()
# test whether more than 0.5 second has passed
elapsed = time.time() - start
if elapsed > 0.5:
    time.sleep(0.5)
start = time.time()


soup = BeautifulSoup(page)

for pin in soup.find_all("div","pin"):
    pinid = "None"
    board = "None"
    source = "None"
    for pinid_a in pin.find_all("a","PinImage ImgLink"):
        pinid = pinid_a['href']
    for clearfix in pin.find_all("div","convo attribution clearfix"):
        for noimage in clearfix.find_all("p","NoImage"):
            for link in noimage.find_all("a"):
                if re.match('/'+user,link['href']):
                    board = link['href']
                else:
                    source = link['href']
    pinids.append(pinid)
    boards.append(board)
    sources.append(source)



print "pinids: " + str(len(pinids))
print "boards: " + str(len(boards))
print "sources: " + str(len(sources))

allpins = zip(pinids,boards,sources)
pp.pprint(sources)
#for page in npages:
    # extract the folder, pin id, and source
