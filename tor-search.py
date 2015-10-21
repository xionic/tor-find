import requests
from pprint import pprint
import sys
import re
import urllib

#config
dl_dir = '/tmp'

def print_debug(msg):
	print msg

def print_item(d):
	print "score:", d["score"], "\tseeds:",d["seeds"], "\ttitle:", d["title"]

class URLOpenerUA(urllib.FancyURLopener):
	version = 'Wget/1.16 (linux-gnu)'

#set UA for downloads
urllib._urlopener = URLOpenerUA()

def download(d):
	url = "http://torcache.net/torrent/" + d["torrent_hash"] +".torrent"
	print_debug("url: " + url)
	urllib.urlretrieve (url, dl_dir + '/' + d["torrent_hash"] + ".torrent")

name = sys.argv[1]
season = sys.argv[2]
episode = sys.argv[3]

search_term = name + " S" + season.zfill(2) + "E" + episode.zfill(2)
url = "https://torrentproject.se/?s=" + search_term + "&orderby=seeders&out=json"

print_debug("Searching for '" + search_term + "'")
headers = {'User-Agent' : 'Wget/1.16 (linux-gnu)'}
r = requests.get(url, headers=headers)

#pprint(r.text)

data_dict = r.json()
#pprint(data_dict)
#convert to list
data = []
for key,value in data_dict.iteritems():
	#only want the numeric keyed items
	if key.isnumeric():
		data.append(value)
	

#pprint(data[12]);
#pprint(data);

#find a good looking match
seed_weight = 1
episode_id_weight = 100000

#assign a score to the results
for i in range(0,len(data)):
	score = 0
	#score based on seeds
	score += int(data[i]['seeds']) * seed_weight
	
	#score based on name
	#TODO

	#score based on season and episode in name
	regex = r'[^0-9]S?0?' + season + r'[Ex]0?' + episode + r'([^0-9]|$)'
	if not re.search(regex, data[i]["title"], re.I):
		#print_debug("MATCHED", data[str(i)]["title"] + " with " + regex)
		score -= episode_id_weight
		
	data[i]['score'] = score

data = sorted(data, key=lambda k: k['score'], reverse=True)

#do we want the top scorer?
print "Download best match?"
print_item(data[0])
print "[y]es, [n]o, [s]show me others"

answer = raw_input()

if answer == "y":
	print_debug(data[0])
	download(data[0])
elif answer == "n":
	sys.exit(0)
elif answer == "s":
	pass
else:
	print "Invalid choice:", answer






























