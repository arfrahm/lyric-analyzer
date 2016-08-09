import urllib2
opener = urllib2.build_opener()
opener.addheaders = [("user-agent","Chrome/18.0.1025.133")]
response = opener.open('http://genius.com/tags/country/all')
songList_html = response.read()
with open("list.txt", 'w') as outfile:
	outfile.write(songList_html)


