# Import needed libraries
import urllib2
import time
import sys
from bs4 import BeautifulSoup

# Set variables
genre = "country"
list_url = "http://genius.com/tags/" + genre + "/all"
user_agent = [("user-agent", "Chrome/18.0.1025.133")]

# Create an opener that has our browser user-agent to prevent being denied
opener = urllib2.build_opener()
opener.addheaders = user_agent


# Open the current page in list, extract information, and then go to the
# next one


# while page_count < 51:

# Use opener to open the specified URL, read the response into a variable
words_used = {}
song_count = 0
for page_count in range(50):
    response = opener.open(list_url + "?page=" + str(page_count + 1))
    songList_html = response.read()
    response.close()
    soup = BeautifulSoup(songList_html, 'html.parser')
    for link in soup.find_all(attrs={"class": "song_link"}):
        songtext = True
        start_time = time.time()
        songlink = link.get("href")
        songopener = urllib2.build_opener()
        songopener.addheaders = user_agent
        songresponse = songopener.open(songlink)
        songhtml = songresponse.read()
        songresponse.close()
        songsoup = BeautifulSoup(songhtml, 'html.parser')
        lyrics = songsoup.find(attrs={"class": "lyrics"}).get_text()
        word_count = 0
        song_count += 1
        for word in lyrics.split(" "):
            if("[" in word):
                songtext = False
            elif("]" in word and not songtext):
                songtext = True

            if("googletag." in word):
                continue
            if(songtext):
                if(word in words_used):
                    words_used[word] += 1
                else:
                    words_used[word] = 1

            word_count += 1

        print "Analyzed " + str(word_count) + " words in " + str(time.time() - start_time) + "s :"
        print "\t" + songlink
        print "Total analyzed: " + str(song_count) + "\n"


with open("lyriclist.txt", 'w') as outfile:
    for key in sorted(words_used, key=words_used.get):
      #  outfile.write(key.encode('utf-8') + ',' + str(words_used[key]))
        outfile.write(key.encode('utf-8'))
        outfile.write(',')
        outfile.write(str(words_used[key]))
        outfile.write('\n')
