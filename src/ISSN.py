from bs4 import BeautifulSoup
import urllib2, sys
import json
import os
import re
import unicodedata
import ast

baseurl='http://dl.acm.org/'
author_map = {}
y = 0
def ckdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except Exception:
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def text_to_id(text):
    text = strip_accents(text.lower())
    text = re.sub('[ ]+', '_', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    return text

def get_soup(aurl):
	hdr = {'User-Agent':'Mozilla/5.0'}
	req = urllib2.Request(aurl,headers=hdr)
	page = urllib2.urlopen(req)	
	asoup = BeautifulSoup(page, 'html.parser')
	return asoup

url = 'http://dl.acm.org/pub_series.cfm?id=J1156&_cf_containerId=pubs&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=C37F87628DE0E7610F1187FC299D1CA1&_cf_rc=1'
soup = get_soup(url)    
posts = soup.find_all("a")
"""
for post in posts[2:3:]:
    if post.get_text() == 'Issue-in-Progress' :
        print('Dont take')
    else :
        link = post["href"]
        newurl = baseurl + link
        newsoup = get_soup(newurl)
        print(newurl)
"""
link = posts[4]["href"]
newurl = baseurl + link  #+ '&preflayout=flat'
newsoup = get_soup(newurl)
table = newsoup.find('table', {'style':'margin-top: 10px'})
issn = table.find_all('td')
print(issn[5].get_text().split('ISSN:')[2].strip())
#fl = open('htmlpage.txt','w')
#fl.write(str(posts))
#fl.write(newsoup.prettify())
#fl.close()