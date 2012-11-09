import urllib
import re
from bs4 import BeautifulSoup
import math
import time

user = "calistoddard"
pinurl = "http://pinterest.com"

firstpg = urllib.urlopen(pinurl + "/" + user + "/pins/?page=2")
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
for pin in soup.find_all("a","PinImage ImgLink"):
    pinids.append(pin['href'])

for item in soup.find_all("div","pin"):   
    sourcenext = -1
    for child in item.descendants:
        tagtext = child.string if not str(child.string)=="None" else "YOUWILLNEVERFINDTHIS"
        print tagtext.decode('utf-8')
        if re.match(ur'<a class="" href="/'+user,tagtext, re.UNICODE):
            boards.append(tagtext)
        if sourcenext == 1:
            sources.append(tagtext)
            sourcenext = 0
        if re.match(' from',tagtext, re.UNICODE):
            sourcenext = 1
    if sourcenext == -1:
        sources.append("None")

        
allpins = zip(pinids,boards,sources)
print allpins
#for page in npages:
    # extract the folder, pin id, and source
