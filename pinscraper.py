import urllib
import BeautifulSoup from bs4
import math

user = "calistoddard"
pinurl = "http://pinterest.com"


firstpg = urllib.open(pinurl + "/" + user + "/pins/")

# get total number of pins from first page
pincount = 0 #fix

# 
npages = math.ceiling(pincount / 50)
for page in npages:
    # extract the folder, pin id, and source


