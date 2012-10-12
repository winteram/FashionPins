import mechanize

user = "calistoddard"
pinurl = "http://pinterest.com"

br = mechanize.Browser()
br.open(pinurl + "/" + user)

# get folders matching particular folder name
# will want to change to getting just folder folders
folders = br.links(url_regex=user,text_regex='\xc2\xa0')
folderlinks = []
pinurls = []
for folder in folders:
    folderlinks.append(folder.url)

for folderlink in folderlinks:
    br.open(pinurl + folderlink)
    # get pins in folder
    pins = br.links(url_regex="^/pin")
    for pin in pins:
        print  '"' + folderlink + '","' + pin.url  + '","' + pin.text + '"'


